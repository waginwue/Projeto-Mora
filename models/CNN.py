# models/CNN.py

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import os


# ============================================================
#  CNN Architecture
# ============================================================

class MoraCNN(nn.Module):
    """
    CNN simples para classificação de defeitos/estados de máquinas
    no projeto MORA.
    """

    def __init__(self, num_classes: int):
        super(MoraCNN, self).__init__()

        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)

        self.pool = nn.MaxPool2d(2, 2)

        self.fc1 = nn.Linear(128 * 16 * 16, 256)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # 64x64 → 32x32
        x = self.pool(F.relu(self.conv2(x)))  # 32x32 → 16x16
        x = self.pool(F.relu(self.conv3(x)))  # 16x16 → 8x8

        x = x.view(-1, 128 * 16 * 16)

        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return x


# ============================================================
#  Preprocessing Pipeline
# ============================================================

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])


# ============================================================
#  Label Mapping (CNN output → Ontology class)
# ============================================================

LABELS = [
    "Normal",
    "Perto_de_Quebrar",
    "Quebrado",
    "X_Quebrado",
    "Y_Quebrado",
    "Z_Quebrado",
]

# Inverse mapping for CNN output
IDX_TO_LABEL = {i: label for i, label in enumerate(LABELS)}


# ============================================================
#  CNN Wrapper
# ============================================================

class CNNModel:
    """
    Wrapper que integra:
    - carregamento do modelo
    - predição
    - conversão para classes OWL (nomes)
    """

    def __init__(self, model_path: str = None):
        self.num_classes = len(LABELS)
        self.model = MoraCNN(self.num_classes)

        if model_path and os.path.exists(model_path):
            self.load_model(model_path)

        self.model.eval()

    # -----------------------------------------------
    def load_model(self, path: str):
        """Carrega pesos .pt ou .pth do PyTorch"""
        self.model.load_state_dict(torch.load(path, map_location="cpu"))

    # -----------------------------------------------
    def predict(self, image_path: str) -> str:
        """
        Recebe o caminho de uma imagem e retorna
        a classe OWL correspondente.
        """

        image = Image.open(image_path).convert("RGB")
        tensor = transform(image).unsqueeze(0)  # Add batch dimension

        with torch.no_grad():
            outputs = self.model(tensor)
            _, predicted = torch.max(outputs, 1)
            label_index = predicted.item()

        return IDX_TO_LABEL[label_index]

    # -----------------------------------------------
    def train(self, dataloader, epochs=10, lr=0.001, device="cpu"):
        """
        Treino simples usando CrossEntropy.
        Dataloader deve ser de (imagem, label)
        """

        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.model.to(device)

        self.model.train()
        for epoch in range(epochs):
            total_loss = 0

            for images, labels in dataloader:
                images, labels = images.to(device), labels.to(device)

                optimizer.zero_grad()
                outputs = self.model(images)

                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            print(f"Epoch {epoch+1}/{epochs} | Loss = {total_loss:.4f}")

        self.model.eval()

    # -----------------------------------------------
    def save(self, path: str):
        """Salva os pesos do modelo"""
        torch.save(self.model.state_dict(), path)

