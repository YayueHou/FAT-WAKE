import numpy
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.onnx 
import numpy as np


# CNN net
class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
    
        self.code = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=8, kernel_size=2, stride=1,padding=1), 
            nn.BatchNorm1d(8),
            nn.ReLU(True),

            nn.MaxPool1d(kernel_size=2, stride=1,padding=1),  

            nn.Conv1d(in_channels=8, out_channels=16, kernel_size=2, stride=1,padding=1), 
            nn.BatchNorm1d(16),
            nn.ReLU(True),
          #  nn.Sigmoid(),
            nn.MaxPool1d(kernel_size=2, stride=1,padding=1), 

      
            nn.Flatten(),
            nn.Linear(in_features=448, out_features=128),
            nn.ReLU(True),
            nn.Linear(in_features=128, out_features=64),
            nn.ReLU(True),
            nn.Linear(in_features=64, out_features=2), 
            nn.Softmax(dim=1) 
        )
 
    def forward(self, x):
        x = self.code(x)
 
        return x
 




def SaveEEGCNNModel(net,savepath):

    torch.save(net,savepath+"/model.pth")
    model =torch.load(savepath+"/model.pth") 

    batch_size = 30 
    input_shape = (1, 24)  

    model.eval()

    x = torch.randn(batch_size, *input_shape)	
    export_onnx_file = savepath+"/model.onnx"		
    torch.onnx.export(model,
                    x,
                    export_onnx_file,
                    opset_version=10,
                    do_constant_folding=True,	
                    input_names=["input"],	
                    output_names=["output"],	
                    dynamic_axes={"input":{0:"batch_size"}, 
                                  "output":{0:"batch_size"}})

def FW_classby_CNN(net,x,y):
  #print(x.shape)
  ave_acc=[]
  for fold in range(10):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    x_train = torch.Tensor(x_train)
    y_train = torch.LongTensor(y_train)
    dataset_train = torch.utils.data.TensorDataset(x_train, y_train)
    data_train = torch.utils.data.DataLoader(dataset_train, batch_size=30, shuffle=True)

    x_test = torch.Tensor(x_test)
    x_test_usq = x_test.unsqueeze(1)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.001)
    # optimizer = torch.optim.SGD(net.parameters(), lr=0.001)

    epochs = 100
    loss_train = []
    for epoch in range(epochs):
      net.train()
      running_loss = 0.0
      for batch_idx, data in enumerate(data_train):
          input_data = data[0]
          input_data = input_data.unsqueeze(1) 
          label = data[1]
          output_data = net(input_data)
          loss = criterion(output_data, label)
          optimizer.zero_grad()
          loss.backward()
          optimizer.step()
          running_loss += loss.item()

      # print("epoch: %d"%epoch, "loss: %f"%(running_loss / len(data_train)))
      loss_train.append(running_loss / len(data_train))

    output_test = net(x_test_usq)
    output_test_ = torch.argmax(output_test,1)
    y_predict = output_test_.detach().numpy().reshape(-1)
    acc_test = [((np.sum(y_predict == y_test)) / x_test.shape[0]) * 100]
    #print("acc test:",acc_test)
    ave_acc.append(acc_test)

  ave_acc=numpy.array(ave_acc)
  # print("acc: ",ave_acc.mean()," std_acc: ",ave_acc.std())
  return ave_acc





