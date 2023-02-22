import torch.nn.functional as F
import torch.nn as nn


class MedNet(nn.Module):
    def __init__(self, xDim, yDim, numC, n_dropout, n_kernels):
        super(MedNet, self).__init__()

        # Convolutional layers + + batch norm + maxpool2d layer
        self.conv1 = nn.Conv2d(1, n_kernels, 7)
        self.bn1 = nn.BatchNorm2d(n_kernels)
        self.conv2 = nn.Conv2d(n_kernels, n_kernels * 2, 7)
        self.bn2 = nn.BatchNorm2d(n_kernels * 2)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=1)

        # Fullies connected layers
        numNodesToFC = 1458 * n_kernels
        self.ful1 = nn.Linear(numNodesToFC, 200)
        self.dropout1 = nn.Dropout(n_dropout)
        self.ful2 = nn.Linear(200, 50)
        self.dropout2 = nn.Dropout(n_dropout)
        self.ful3 = nn.Linear(50, numC)

    def forward(self, x):
        # Apply activations for convolutional layers
        x = F.elu(self.conv1(x))
        x = self.bn1(x)
        x = F.elu(self.conv2(x))
        x = self.bn2(x)
        x = self.pool(x)

        # Flatten convolutional layer into fully connected layer
        x = x.view(-1, self.num_flat_features(x))

        # Apply activations for fullies connected layers
        x = F.elu(self.ful1(x))
        x = self.dropout1(x)
        x = F.elu(self.ful2(x))
        x = self.dropout2(x)

        # Final FC layer to output. No activation, because it's used to calculate loss
        x = self.ful3(x)

        return x

    def num_flat_features(self, x):
        # Count the individual nodes in a layer
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
