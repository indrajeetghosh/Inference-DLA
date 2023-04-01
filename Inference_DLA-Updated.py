{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "84bfa9d6-0345-4103-b646-2ed24e35cdc1",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "from sklearn.preprocessing import MinMaxScaler  \n",
    "import os\n",
    "import itertools\n",
    "from sklearn.metrics import mean_squared_error, r2_score\n",
    "from sklearn.model_selection import train_test_split\n",
    "\n",
    "import torch.nn.functional as F\n",
    "from tqdm import tqdm, tqdm_notebook\n",
    "import torch.nn as nn\n",
    "from torch.autograd import Variable as V\n",
    "from torch.autograd import grad\n",
    "from torch.utils.data import DataLoader,Dataset, TensorDataset\n",
    "seed = 42\n",
    "import torch\n",
    "from torch.nn import Linear, ReLU, MSELoss, Sequential, Conv1d, MaxPool1d, Module, Softmax, BatchNorm1d, Dropout\n",
    "import torchvision.models as models\n",
    "import torch.optim as optim\n",
    "\n",
    "from Model import MultiTask\n",
    "from multi_output_data_prep import MultiOutputDataset\n",
    "from losses import XSigmoidLoss, LogCoshLoss, AlgebraicLoss\n",
    "\n",
    "\n",
    "### Checking GPU avaliable ###\n",
    "#device = torch.device(\"cuda:0\" if torch.cuda.is_available() else \"cpu\")\n",
    "#print(device)\n",
    "\n",
    "## DATA - Features and Score\n",
    "\n",
    "X = np.load('X_inference.npy')\n",
    "Y = np.load('Y_inference.npy')\n",
    "\n",
    "##  Train and Test Sp\n",
    "\n",
    "X_train ,X_test ,trn_y,val_y = train_test_split(X,Y,test_size=0.10)\n",
    "\n",
    "y1_test = val_y[:,0]\n",
    "y2_test = val_y[:,1]\n",
    "y3_test = val_y[:,2]\n",
    "y4_test = val_y[:,3]\n",
    "\n",
    "test_loader = DataLoader(dataset=MultiOutputDataset(X_test, y1_test, y2_test, y3_test, y4_test), shuffle=False, batch_size=500)\n",
    "\n",
    "dataiter = iter(test_loader)\n",
    "data, label1, label2, label3,label4 = dataiter.next()\n",
    "print(type(data))\n",
    "print(data.shape)\n",
    "print(label1.shape)\n",
    "print(label2.shape)\n",
    "\n",
    "model = MultiTask()\n",
    "\n",
    "# Load the saved model checkpoint\n",
    "PATH = \"Saved_Trained_Model.pth\"\n",
    "model.load_state_dict(torch.load(PATH))\n",
    "\n",
    "# Define your loss functions for each task\n",
    "criterion1 = LogCoshLoss() \n",
    "criterion2 = LogCoshLoss()\n",
    "criterion3 = LogCoshLoss()\n",
    "criterion4 = LogCoshLoss()\n",
    "\n",
    "# Instantiate the optimizer\n",
    "optimizer = optim.Adam(model.parameters(), lr=1e-5)\n",
    "num_epochs = 5\n",
    "\n",
    "# Set the model to evaluation mode\n",
    "for epoch in range(num_epochs):\n",
    "    model.eval()\n",
    "\n",
    "# Evaluate the model on a validation dataset\n",
    "    with torch.no_grad():\n",
    "        task1_losses = []\n",
    "        task2_losses = []\n",
    "        task3_losses = []\n",
    "        task4_losses = []\n",
    "    \n",
    "        for data, target1, target2, target3, target4  in test_loader:\n",
    "            data, target1, target2, target3, target4 = data.to(device), target1.float().to(device), target2.float().to(device), target3.float().to(device), target4.float().to(device)\n",
    "            output1, output2, output3, output4 = model(data)\n",
    "    \n",
    "            test_loss_1 = criterion1(output1.squeeze(), target1)\n",
    "            test_loss_2 = criterion2(output2.squeeze(), target2)\n",
    "            test_loss_3 = criterion3(output3.squeeze(), target3)\n",
    "            test_loss_4 = criterion4(output4.squeeze(), target4)\n",
    "        \n",
    "        \n",
    "        # Calculate the loss for each task and append it to the list of losses\n",
    "            task1_losses.append(test_loss_1.item())\n",
    "            task2_losses.append(test_loss_2.item())\n",
    "            task3_losses.append(test_loss_3.item())\n",
    "            task4_losses.append(test_loss_4.item())\n",
    "\n",
    "    # Calculate the average loss for each task\n",
    "        avg_task1_loss = sum(task1_losses) / len(task1_losses)\n",
    "        avg_task2_loss = sum(task2_losses) / len(task2_losses)\n",
    "        avg_task3_loss = sum(task3_losses) / len(task3_losses)\n",
    "        avg_task4_loss = sum(task4_losses) / len(task4_losses)\n",
    "\n",
    "    \n",
    "        print(f\"Task 1 validation loss: {avg_task1_loss}\")\n",
    "        print(f\"Task 2 validation loss: {avg_task2_loss}\")\n",
    "        print(f\"Task 1 validation loss: {avg_task3_loss}\")\n",
    "        print(f\"Task 2 validation loss: {avg_task4_loss}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d22621c7-da41-4275-9f6f-6edb10c4f646",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9d3c72e6-67bd-4c5f-982e-371aa96cfffb",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "0a81ab4d-ec21-4d4c-ab29-e3dda6aa3add",
   "metadata": {},
   "outputs": [],
   "source": [
    "X = np.load('X_inference.npy')\n",
    "Y = np.load('Y_inference.npy')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "fd446893-acff-44b7-9fca-b4d9c6b02c19",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(2000, 256, 12)"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "84b4a402-a238-4d8f-b91e-3d880227ef59",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(2000, 4)"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "Y.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "64101ace-e688-4085-80d4-a3c2460f6a73",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train ,X_test ,trn_y,val_y = train_test_split(X,Y,test_size=0.10)\n",
    "\n",
    "y1_test = val_y[:,0]\n",
    "y2_test = val_y[:,1]\n",
    "y3_test = val_y[:,2]\n",
    "y4_test = val_y[:,3]\n",
    "\n",
    "test_loader = DataLoader(dataset=MultiOutputDataset(X_test, y1_test, y2_test, y3_test, y4_test), shuffle=False, batch_size=500)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "c64829c4-38db-46fa-b8bc-19abac1dd64c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'torch.Tensor'>\n",
      "torch.Size([200, 256, 12])\n",
      "torch.Size([200])\n",
      "torch.Size([200])\n"
     ]
    }
   ],
   "source": [
    "dataiter = iter(test_loader)\n",
    "data, label1, label2, label3,label4 = dataiter.next()\n",
    "print(type(data))\n",
    "print(data.shape)\n",
    "print(label1.shape)\n",
    "print(label2.shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "6f65fa1a-af5c-489b-8b32-b1409a37a365",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "cuda:0\n"
     ]
    }
   ],
   "source": [
    "device = torch.device(\"cuda:0\" if torch.cuda.is_available() else \"cpu\")\n",
    "print(device)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1b3462f5-1ce6-400d-a249-cbac7705c5f7",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
