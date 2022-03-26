import torch
import torch.nn as nn
from torchvision import transforms, utils, datasets
from torch.autograd import Variable
from PIL import Image


class ClassificationModel:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.load(model_path,  map_location=torch.device(self.device))
        self.model.eval()

    def predict_image(self, image):
        input = Variable(self.transform_image(image))
        input = input.to(self.device)
        output = self.model(input)
        output=torch.sigmoid(output)
        output=float(output)
        return 1-output

    @staticmethod
    def transform_image(image):
        test_transforms = transforms.Compose([transforms.Resize(224),
                                      transforms.ToTensor(),
                                     ])
        image_tensor = test_transforms(image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        return image_tensor
