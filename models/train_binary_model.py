import math
import torch  # for AI
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchmetrics import R2Score
import matplotlib.pyplot as plt  # to plot training


class CustomTopicDataset(Dataset):  # the dataset class
    def __init__(self, sentences, labels):
        self.x = sentences
        self.y = labels
        if isinstance(self.x, list):
            self.length = len(self.x)
            self.shape = len(self.x[0])
        else:
            self.length = self.x.shape[0]
            self.shape = self.x[0].shape[0]
        self.feature_names = ['sentences', 'labels']

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


class NeuralNetwork(nn.Module):  # the NN with linear relu layers and one sigmoid in the end
    def __init__(self, input_size):
        super().__init__()
        self.linear_relu_stack_with_sigmoid = nn.Sequential(
            nn.Linear(input_size, 4096),
            nn.ReLU(),
            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Linear(4096, 2048),
            nn.ReLU(),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        logits = self.linear_relu_stack_with_sigmoid(x)
        return logits


class History:  # The history object to keep track of metrics during training and plot graphs to it.
    def __init__(self, val_set, train_set, model, **kwargs):  # kwargs are the metrics to keep track of.
        self.val_set = val_set
        self.train_set = train_set
        self.model = model
        self.kwargs = kwargs
        self.history = {'steps': []}
        for i in kwargs.keys():
            self.history.update({'val_' + i: []})
            self.history.update({'tra_' + i: []})
        self.valloader = None
        self.trainloader = None

    def save(self, step):  # this function is called in the training loop to save the current state of the model.
        short_history = {}
        for i in self.kwargs.keys():
            short_history.update({'val_' + i: []})
            short_history.update({'tra_' + i: []})
        # generate two dataloader with each k entries from either the training or the validation data.
        k = 500
        short_train_set, waste = torch.utils.data.random_split(self.train_set, [k, len(self.train_set) - k])
        short_val_set, waste = torch.utils.data.random_split(self.val_set, [k, len(self.val_set) - k])
        self.valloader = DataLoader(dataset=short_val_set, batch_size=5, shuffle=True, num_workers=2)
        self.trainloader = DataLoader(dataset=short_train_set, batch_size=5, shuffle=True, num_workers=2)
        # iterate over both dataloaders simultaneously
        for i, ((val_in, val_label), (tra_in, tra_label)) in enumerate(zip(self.valloader, self.trainloader)):
            with torch.no_grad():
                self.model.eval()
                # predict outcomes for training and validation.
                val_pred = self.model(val_in)
                tra_pred = self.model(tra_in)
                for j in self.kwargs.keys():  # iterate over the metrics
                    # calculate metric and save to short history
                    if len(val_pred) > 1:
                        val_l = self.kwargs[j](val_pred, val_label).item()
                        tra_l = self.kwargs[j](tra_pred, tra_label).item()
                        short_history['val_' + j].append(val_l)
                        short_history['tra_' + j].append(tra_l)
                self.model.train()
        # iterate over metrics and save the average of the short history to the history.
        for i in self.kwargs.keys():
            self.history['val_' + i].append(sum(short_history['val_' + i]) / len(short_history['val_' + i]))
            self.history['tra_' + i].append(sum(short_history['tra_' + i]) / len(short_history['tra_' + i]))
        self.history['steps'].append(step)  # save steps for the x-axis

    # this function is called after training to generate graphs.
    # When path is given, the graphs are saved and plt.show() is not called.
    def plot(self, path=None):
        figures = []
        for i in self.kwargs.keys():  # iterate over the metrics and generate graphs for each.
            fig, ax = plt.subplots()
            ax.plot(self.history['steps'], self.history['val_' + i], 'b')
            ax.plot(self.history['steps'], self.history['tra_' + i], 'r')
            ax.set_title(i.upper())
            ax.set_ylabel(i)
            ax.set_xlabel('Epochs')
            figures.append(fig)
            if path is None:
                plt.show()  # depending on the setup the graphs might still be shown even without this function called.
            else:
                plt.savefig(f"{path}/{i}")
            plt.clf()
        return figures


# convert embedded data to a proper dataset
def to_dataset(embedded_data):
    def transpose(lst):
        return list(map(list, zip(*lst)))

    embedded_data = transpose(embedded_data)
    labels = embedded_data[1]
    sentences = embedded_data[0]
    labels = [torch.tensor([1.]) if i else torch.tensor([0.]) for i in labels]
    dataset = CustomTopicDataset(sentences, labels)
    return dataset


# this function trains a model and returns it as well as the history object of its training process.
def train(dataset, epochs=10, lr=0.001, val_frac=0.1, batch_size=25, loss=nn.BCELoss(), **kwargs):
    # get_acc measures the accuracy and is passed as a metric to the history object.
    def get_acc(pred, target):
        pred_tag = torch.round(pred)

        correct_results_sum = (pred_tag == target).sum().float()
        acc = correct_results_sum / target.shape[0]
        acc = torch.round(acc * 100)

        return acc

    # generate validation dataset with the fraction of entries of the full set passed as val_frac
    val_len = int(round(len(dataset) * val_frac))
    train_set, val_set = torch.utils.data.random_split(dataset, [len(dataset) - val_len, val_len])
    dataloader = DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
    print(f'Datasetshape: {dataset.shape}')
    model = NeuralNetwork(dataset.shape)

    loss = loss  # the loss passed to this train function
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    # define metrics to be monitored by the history object during training.
    r2loss = R2Score()
    mseloss = nn.MSELoss()
    bceloss = nn.BCELoss()
    accuracy = get_acc

    history = History(val_set, train_set, model, r2loss=r2loss, mseloss=mseloss, accuracy=accuracy, bceloss=bceloss, **kwargs)  # define history object

    # main training loop
    for epoch in range(epochs):
        running_loss = []
        print(f'Starting new epoch {epoch + 1}/{epochs}')
        for step, (inputs, labels) in enumerate(dataloader):
            y_pred = model(inputs)
            lo = loss(y_pred, labels)
            lo.backward()
            optimizer.step()
            optimizer.zero_grad()
            running_loss.append(lo.item())
            if (step + 1) % math.floor(len(dataloader) / 5 + 2) == 0:  # if (step+1) % 100 == 0:
                print(f'current loss:\t\t{sum(running_loss) / len(running_loss)}')
                running_loss = []
                history.save(epoch + step / len(dataloader))
                # save current state of the model to history
    # generate folder with timestamp and save the model there.
    # now = str(d.now().isoformat()).replace(':', 'I').replace('.', 'i').replace('-', '_')
    # os.mkdir(f"model_{now}")
    torch.save(model, f"secret_model.pt")
    #print(f'Model saved to "model_{now}/model.pt"')
    # history.plot(f"model_{now}")  # save graphs to the folder
    return history, model  # return history and model


# with this function you can pass custom sentences to the model

def get_embedded():
    return torch.load(f"data_secrets_found_openai_embedded.pt")
    # return torch.load(f"data_go_to_binary_openai_embedded.pt")


if __name__ == "__main__":
    embedded_data = get_embedded()
    dataset = to_dataset(embedded_data)
    history, model = train(dataset=dataset, epochs=10, lr=0.0001, val_frac=0.1, batch_size=10, loss=nn.BCELoss())
    history.plot()

