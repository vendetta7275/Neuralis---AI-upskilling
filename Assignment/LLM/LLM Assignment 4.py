import os
import gc
import sys
import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer


# LOCAL ENVIRONMENT & AUTHENTICATION SETUP

if "HF_TOKEN" not in os.environ:
    print(" Tip: Set your Hugging Face token in your terminal environment variables: export HF_TOKEN='your_token'")
  

MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"

TEST_PROMPTS = [
    "Explain the concept of asynchronous core hours in a remote company.",
    "Write a python function to compute cross-entropy loss given logits and labels.",
    "Give me three clear tips to prevent data leakage during feature scaling."
]

def get_instruction_dataset():
    """Generates a small instruction dataset to facilitate swift pipeline training."""
    data = {
        "text": [
            "Instruction: Explain remote work benefits. Response: Remote work optimizes global operational scaling, eliminates standard physical workspace dependencies, and unlocks production autonomy.",
            "Instruction: What does StandardScaler do? Response: StandardScaler rescales data dimensions so they share a mean of zero and a standard variance of 1, shielding math models from feature magnitude imbalances.",
            "Instruction: Define machine learning validation. Response: Validation splits a data footprint early into 80% training and 20% testing blocks, ensuring testing observations remain isolated from parameters."
        ]
    }
    return Dataset.from_dict(data)

def get_peak_vram(label: str) -> float:
    """Accurately calculates peak GPU memory allocation in Gigabytes."""
    if torch.cuda.is_available():
        peak_bytes = torch.cuda.max_memory_allocated()
        peak_gb = peak_bytes / (1024 ** 3)
        print(f" [{label}] Peak GPU Memory Registered: {peak_gb:.3f} GB")
        return round(peak_gb, 3)
    print(f" [{label}] CUDA is unavailable. Tracking metrics on CPU/Host Memory.")
    return 0.0

def clear_system_cache():
    """Flushes active tensors from VRAM to completely isolate LoRA from QLoRA steps."""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()


# FINETUNING WORKFLOW WRAPPER
def execute_peft_training(use_4bit_qlora: bool) -> dict:
    experiment_mode = "QLoRA (4-bit)" if use_4bit_qlora else "LoRA (FP16)"
    print("\n" + "="*70)
    print(f" EXECUTING EXPERIMENT TRACKING FOR: {experiment_mode.upper()}")
    print("="*70)
    
    # Local Safeguard: bitsandbytes 4-bit quantization requires CUDA
    if use_4bit_qlora and not torch.cuda.is_available():
        print(f" Skipping {experiment_mode}: 4-bit quantization requires an NVIDIA GPU with CUDA.")
        return {
            "trainable_parameters": 0,
            "final_loss": 0.0,
            "peak_vram_gb": 0.0,
            "outputs": ["Skipped due to lack of CUDA hardware."] * len(TEST_PROMPTS)
        }

    clear_system_cache()
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    except Exception as e:
        print(f" Error loading model/tokenizer. Ensure you are logged into Hugging Face or HF_TOKEN is set correctly.\nDetails: {e}")
        sys.exit(1)

    tokenizer.pad_token = tokenizer.eos_token
    
    # Branching: Establish Quantization configurations strictly for QLoRA
    if use_4bit_qlora:
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            quantization_config=quant_config,
            device_map="auto"
        )
        # Prepare quantized model layers securely for backpropagation steps
        model = prepare_model_for_kbit_training(model)
    else:
        # Locally, fallback to float32 if CUDA is not present to avoid unsupported device_map or type errors
        compute_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        device_layout = "auto" if torch.cuda.is_available() else None
        
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=compute_dtype,
            device_map=device_layout
        )

    # Core LoRA Parameters requested by Assignment Specs
    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"], 
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, peft_config)
    
    # Calculate parameter allocations
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f" Trainable Parameters Count: {trainable_params:,}")
    
    # Set standard shared hyperparameter limits
    training_args = TrainingArguments(
        output_dir=f"./output_{'qlora' if use_4bit_qlora else 'lora'}",
        num_train_epochs=2,
        per_device_train_batch_size=1,
        learning_rate=2e-4,
        weight_decay=0.01,
        fp16=torch.cuda.is_available(),  # Set to False automatically if running locally on CPU
        logging_steps=1,
        save_strategy="no",
        report_to="none"
    )
    
    trainer = SFTTrainer(
        model=model,
        train_dataset=get_instruction_dataset(),
        dataset_text_field="text",
        max_seq_length=128,
        args=training_args
    )
    
    print(f" Training model under {experiment_mode} conditions...")
    history = trainer.train()
    final_loss = history.training_loss
    print(f" Final Logged Loss: {final_loss:.4f}")
    
    peak_memory = get_peak_vram(experiment_mode)
    
    # Qualitative Evaluation Step
    print(f"\n Generating Comparative Test Responses for {experiment_mode}:")
    model.eval()
    test_responses = []
    
    for prompt in TEST_PROMPTS:
        formatted_input = f"Instruction: {prompt}\nResponse:"
        inputs = tokenizer(formatted_input, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=50, 
                pad_token_id=tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.7
            )
        decoded_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"\n Prompt: {prompt}\n✨ Generated Output:\n{decoded_text}\n" + "-"*40)
        test_responses.append(decoded_text)
        
    return {
        "trainable_parameters": trainable_params,
        "final_loss": final_loss,
        "peak_vram_gb": peak_memory,
        "outputs": test_responses
    }


# PIPELINE EXECUTION & COMPARATIVE REPORTING
if __name__ == "__main__":
    # Run Phase 1: Standard LoRA Fine-Tuning
    lora_results = execute_peft_training(use_4bit_qlora=False)
    
    # Run Phase 2: QLoRA Fine-Tuning 
    qlora_results = execute_peft_training(use_4bit_qlora=True)
    
    # Print out Final Summary Table
    print("\n" + "="*70)
    print(" OVERALL ASSIGNMENT PEFT METRIC COMPARISON")
    print("="*70)
    print(f"{'Performance Metric':<25} | {'LoRA (FP16)':<18} | {'QLoRA (4-bit)':<18}")
    print("-"*70)
    print(f"{'Trainable Parameters':<25} | {lora_results['trainable_parameters']:<18,} | {qlora_results['trainable_parameters']:<18,}")
    print(f"{'Final Training Loss':<25} | {lora_results['final_loss']:<18.4f} | {qlora_results['final_loss']:<18.4f}")
    print(f"{'Peak GPU Memory Usage':<25} | {str(lora_results['peak_vram_gb']) + ' GB':<18} | {str(qlora_results['peak_vram_gb']) + ' GB':<18}")
    print("="*70)
    print("\n Key Observation Analysis Note:")
    print("Notice that while the 'Trainable Parameters' count stays completely identical across both frameworks (since the adapter configuration sizes are unchanged), QLoRA achieves a massive drop in peak GPU VRAM consumption. This memory optimization happens because the core 1B base model weight arrays are compressed down into a 4-bit NormalFloat format.")