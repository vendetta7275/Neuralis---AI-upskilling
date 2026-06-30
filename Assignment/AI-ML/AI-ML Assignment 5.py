import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

torch.manual_seed(42)

# 1. DATA LOADING, SPLITTING, AND NORMALIZATION
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

print("--- 1. Data Summary ---")
print(f"Training samples: {len(train_dataset)}")
print(f"Testing samples: {len(test_dataset)}")
print("-" * 40)


# 2. NEURAL NETWORK ARCHITECTURE
class DigitMLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(DigitMLP, self).__init__()
        # Define the structural layers
        self.fc1 = nn.Linear(input_dim, hidden_dim)   
        self.relu = nn.Utils = nn.ReLU()             
        self.fc2 = nn.Linear(hidden_dim, output_dim)   
    def forward(self, x):
        x = x.view(x.size(0), -1) 
        
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out) 
        return out


INPUT_DIM = 28 * 28 
HIDDEN_DIM = 128
OUTPUT_DIM = 10 

model = DigitMLP(input_dim=INPUT_DIM, hidden_dim=HIDDEN_DIM, output_dim=OUTPUT_DIM)


# 3. LOSS FUNCTION, OPTIMIZER, & TRAINING LOOP
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 5

print("\n--- 3. Starting Training Loop ---")
for epoch in range(1, epochs + 1):
    model.train()
    running_loss = 0.0
    
    for batch_idx, (images, labels) in enumerate(train_loader):
        optimizer.zero_grad()
        
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        loss.backward()
        
        optimizer.step()
        
        running_loss += loss.item()
        
    epoch_loss = running_loss / len(train_loader)
    print(f"Epoch [{epoch}/{epochs}] | Average Training Loss: {epoch_loss:.4f}")

print("-" * 40)


# 4. TEST DATA EVALUATION
model.eval() # Set model to evaluation mode
correct = 0
total = 0

with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        
        _, predicted = torch.max(outputs.data, dim=1)
        
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = (correct / total) * 100

print(f" Final Evaluation Results:")
print(f"Total Test Images evaluated: {total}")
print(f"Correctly Classified: {correct}")
print(f" Test Accuracy: {accuracy:.2f}%")