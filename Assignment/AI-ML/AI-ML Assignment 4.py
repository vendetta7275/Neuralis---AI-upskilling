import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

torch.manual_seed(42)

# 1. DATA PREPARATION
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.long)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

# 2. DEFINING THE MODEL NEURAL NETWORK
class IrisMLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(IrisMLP, self).__init__()
        # Define layers
        self.fc1 = nn.Linear(input_dim, hidden_dim) 
        self.relu = nn.ReLU()                        
        self.fc2 = nn.Linear(hidden_dim, output_dim)   
        
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out) 
        return out


model = IrisMLP(input_dim=4, hidden_dim=16, output_dim=3)


# 3. LOSS FUNCTION & OPTIMIZER
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 4. TRAINING LOOP
epochs = 50

print("--- Starting Training Loop ---")
for epoch in range(1, epochs + 1):
    model.train() 
    running_loss = 0.0
    
    for batch_X, batch_y in train_loader:
        # 1. Clear gradients from the previous step
        optimizer.zero_grad()
        
        # 2. Forward pass
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        
        # 3. Backward pass (Compute gradients)
        loss.backward()
        
        # 4. Update model parameters
        optimizer.step()
        
        running_loss += loss.item() * batch_X.size(0)
        
    epoch_loss = running_loss / len(train_loader.dataset)
    
    # Print status every 10 epochs
    if epoch % 10 == 0 or epoch == 1:
        print(f"Epoch [{epoch:02d}/{epochs}] | Loss: {epoch_loss:.4f}")

print("-" * 40)

# 5. EVALUATION ON TEST DATA
model.eval() # Set model to evaluation mode

with torch.no_grad():
    test_outputs = model(X_test_tensor)
    
    _, predicted = torch.max(test_outputs, dim=1)
    
    correct = (predicted == y_test_tensor).sum().item()
    total = y_test_tensor.size(0)
    accuracy = (correct / total) * 100

print(f" Final Evaluation Results:")
print(f"Total Test Samples: {total}")
print(f"Correctly Predicted: {correct}")
print(f" Test Accuracy: {accuracy:.2f}%")