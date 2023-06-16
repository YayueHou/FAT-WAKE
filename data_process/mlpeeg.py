from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.onnx 
import numpy as np


# 网络
class MLPNet(nn.Module):
    def __init__(self):
        super(MLPNet, self).__init__()
        self.code = nn.Sequential(
            nn.Linear(24,32),  
            nn.ReLU(True),
            nn.Linear(32,32),  
            nn.ReLU(True),
            nn.Linear(32,32), 
            nn.ReLU(True),
            nn.Linear(32,2),  
            nn.Softmax(dim=1) 
        ) 
    def forward(self, x):
        x = self.code(x)
        return x

def MLP_class(net,x,y):
  ave_acc=[]
  for fold in range(10):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    x_train_ = torch.Tensor(x_train)
    y_train_ = torch.Tensor(y_train)
    x_test_ = torch.Tensor(x_test)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.001)
    num_epoch = 2000
    for epoch in range(num_epoch):
      y_p = net(x_train_) 
      loss = criterion(y_p,y_train_.long())
      optimizer.zero_grad()  
      loss.backward()  
      optimizer.step() 
    output_test = net(x_test_)
    output_test_ = torch.argmax(output_test,1)
    y_predict = output_test_.detach().numpy().reshape(-1)
    acc_test = [((np.sum(y_predict == y_test)) / x_test_.shape[0]) * 100]
    ave_acc.append(acc_test)
  ave_acc=np.array(ave_acc)
  return ave_acc


