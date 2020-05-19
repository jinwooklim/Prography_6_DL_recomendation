import torch.nn as nn
import torch
import torch.nn.functional as F


class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()

        self.fc1 = nn.Sequential(
            nn.Linear(6, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, 128))

    def forward_once(self, latitude0, longitude0, latitude1, longitude1, latitude2, longitude2):
        # print("Latitude",Latitude.size())
        # print("Longitude", Longitude.size())

        concated = torch.cat((latitude0, longitude0, latitude1, longitude1, latitude2, longitude2), dim=1)
        # print("A.size()",A.size())

        output = self.fc1(concated)
        return output

    # choice
    def forward(self, alpha_latitude0, alpha_longitude0, alpha_latitude1, alpha_longitude1, alpha_latitude2,
                alpha_longitude2):
        output1 = self.forward_once(alpha_latitude0, alpha_longitude0, alpha_latitude1, alpha_longitude1,
                                    alpha_latitude2, alpha_longitude2)
        
        return output1


class ContrastiveLoss(torch.nn.Module):
    """
    Contrastive loss function.
    Based on: http://yann.lecun.com/exdb/publis/pdf/hadsell-chopra-lecun-06.pdf
    """

    def __init__(self, margin=2.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, output1, output2, label):
        euclidean_distance = F.pairwise_distance(output1, output2, keepdim=True)
        loss_contrastive = torch.mean((1 - label) * torch.pow(euclidean_distance, 2) +
                                      (label) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))

        return loss_contrastive
