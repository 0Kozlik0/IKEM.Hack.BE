import torch.nn as nn
from torchvision import models


# Load Pretrained DeepLabV3+ Model with ResNet Backbone
class DeepLabV3(nn.Module):
    def __init__(self, num_classes=4):
        super(DeepLabV3, self).__init__()
        self.model = models.segmentation.deeplabv3_resnet50(pretrained=True)
        self.model.classifier[4] = nn.Conv2d(256, num_classes, kernel_size=1)
    
    def forward(self, x):
        return self.model(x)['out']