import numpy as np
import pandas as pd
import os
import requests
from matplotlib import pyplot as plt
import warnings


class OneLayerNeural:
    def __init__(self, n_features, n_classes):
        self.n_features = n_features
        self.n_classes = n_classes
        self.weights = xavier(self.n_features, self.n_classes)
        self.biases = xavier(1, self.n_classes)
        self.fwd = None

    def forward(self, X):
        self.fwd = sigmoid((X @ self.weights) + self.biases)

    def backprop(self, X, y, alpha):
        a = np.transpose(X)
        b = sigmoid_diff((X @ self.weights) + self.biases)
        c = cost_function_mse_diff(self.fwd, y)
        gradient_weight = a @ (b * c)
        gradient_biases = np.sum(b * c, axis=0)
        self.weights -= ((gradient_weight / self.fwd.shape[0]) * alpha)
        self.biases -= ((gradient_biases / self.fwd.shape[0]) * alpha)

    def epoch_train(self, X_train, y_train, X_test, y_test, batch, epoch, alpha):
        cost_log = np.array([])
        accuracy_log = np.array([])
        for _ in range(epoch):
            trained_size = 0
            while trained_size < X_train.shape[0]:
                self.forward(X_train[trained_size:trained_size + batch])
                self.backprop(X_train[trained_size:trained_size + batch],
                              y_train[trained_size:trained_size + batch], alpha)
                trained_size += batch
            cost_log = np.append(cost_log, cost_function_mse(self.fwd, y_train[-batch:]))
            accuracy_log = np.append(accuracy_log, self.accuracy(X_test, y_test))
        return accuracy_log

    def accuracy(self, X_test, y_test):
        self.forward(X_test)
        counter = 0
        for i in range(y_test.shape[0]):
            if np.argmax(self.fwd[i]) == np.argmax(y_test[i]):
                counter += 1
        return counter / y_test.shape[0]


class TwoLayerNeural:
    def __init__(self, n_features, n_classes, n_layer_size):
        self.n_features = n_features
        self.n_classes = n_classes
        self.n_layer_size = n_layer_size
        self.weights_first = xavier(self.n_features, self.n_layer_size)
        self.biases_first = xavier(1, self.n_layer_size)
        self.weights_second = xavier(self.n_layer_size, self.n_classes)
        self.biases_second = xavier(1, self.n_classes)
        self.fwd_first = None
        self.fwd_second = None

    def forward(self, X):
        self.fwd_first = sigmoid((X @ self.weights_first) + self.biases_first)
        self.fwd_second = sigmoid((self.fwd_first @ self.weights_second) + self.biases_second)

    def backprop(self, X, y, alpha):
        a2 = np.transpose(self.fwd_first)
        b2 = sigmoid_diff((self.fwd_first @ self.weights_second) + self.biases_second)
        c2 = cost_function_mse_diff(self.fwd_second, y)
        gradient_weight_second = a2 @ (b2 * c2)
        gradient_biases_second = np.sum(b2 * c2, axis=0)
        self.weights_second -= ((gradient_weight_second / self.fwd_second.shape[0]) * alpha)
        self.biases_second -= ((gradient_biases_second / self.fwd_second.shape[0]) * alpha)
        a1 = np.transpose(X)
        b1 = sigmoid_diff((X @ self.weights_first) + self.biases_first)
        c1 = (b2 * c2) @ np.transpose(self.weights_second)
        gradient_weight_first = a1 @ (b1 * c1)
        gradient_biases_first = np.sum(b1 * c1, axis=0)
        self.weights_first -= ((gradient_weight_first / self.fwd_first.shape[0]) * alpha)
        self.biases_first -= ((gradient_biases_first / self.fwd_first.shape[0]) * alpha)

    def epoch_train(self, X_train, y_train, X_test, y_test, batch, epoch, alpha):
        cost_log = np.array([])
        accuracy_log = np.array([])
        for _ in range(epoch):
            trained_size = 0
            while trained_size < X_train.shape[0]:
                self.forward(X_train[trained_size:trained_size + batch])
                self.backprop(X_train[trained_size:trained_size + batch],
                              y_train[trained_size:trained_size + batch], alpha)
                trained_size += batch
            cost_log = np.append(cost_log, cost_function_mse(self.fwd_second, y_train[-batch:]))
            accuracy_log = np.append(accuracy_log, self.accuracy(X_test, y_test))
        plot(list(cost_log), list(accuracy_log))

    def accuracy(self, X_test, y_test):
        self.forward(X_test)
        counter = 0
        for i in range(y_test.shape[0]):
            if np.argmax(self.fwd_second[i]) == np.argmax(y_test[i]):
                counter += 1
        return counter / y_test.shape[0]


def one_hot(data: np.ndarray) -> np.ndarray:
    y_train = np.zeros((data.size, max(data) + 1))
    rows = np.arange(data.size)
    y_train[rows, data] = 1
    return y_train


def plot(loss_history: list, accuracy_history: list, filename='plot'):
    n_epochs = len(loss_history)

    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.plot(loss_history)

    plt.xlabel('Epoch number')
    plt.ylabel('Loss')
    plt.xticks(np.arange(0, n_epochs, 4))
    plt.title('Loss on train dataframe from epoch')
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(accuracy_history)

    plt.xlabel('Epoch number')
    plt.ylabel('Accuracy')
    plt.xticks(np.arange(0, n_epochs, 4))
    plt.title('Accuracy on test dataframe from epoch')
    plt.grid()

    plt.savefig(f'{filename}.png')


def scale(train, test):
    return train / np.max(train), test / np.max(test)


def xavier(n_in, n_out):
    low = -np.sqrt(6 / (n_in + n_out))
    high = np.sqrt(6 / (n_in + n_out))
    return np.random.uniform(low, high, (n_in, n_out))


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_diff(x):
    return sigmoid(x) * (1 - sigmoid(x))


def cost_function_mse(y_activation, y_train):
    return np.mean((y_activation - y_train) ** 2)


def cost_function_mse_diff(y_activation, y_train):
    return 2 * (y_activation - y_train)


if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    if ('fashion-mnist_train.csv' not in os.listdir('../Data') and
            'fashion-mnist_test.csv' not in os.listdir('../Data')):
        print('Train dataset loading.')
        url = "https://www.dropbox.com/s/5vg67ndkth17mvc/fashion-mnist_train.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/fashion-mnist_train.csv', 'wb').write(r.content)
        print('Loaded.')

        print('Test dataset loading.')
        url = "https://www.dropbox.com/s/9bj5a14unl5os6a/fashion-mnist_test.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/fashion-mnist_test.csv', 'wb').write(r.content)
        print('Loaded.')

    warnings.filterwarnings('ignore')

    raw_train = pd.read_csv('../Data/fashion-mnist_train.csv')
    raw_test = pd.read_csv('../Data/fashion-mnist_test.csv')

    X_train = raw_train[raw_train.columns[1:]].values
    X_test = raw_test[raw_test.columns[1:]].values

    y_train = one_hot(raw_train['label'].values)
    y_test = one_hot(raw_test['label'].values)

    X_train_scaled, X_test_scaled = scale(X_train, X_test)

    two_layer = TwoLayerNeural(X_train_scaled.shape[1], 10, 64)
    two_layer.epoch_train(X_train_scaled, y_train, X_test, y_test, 100, 20, 0.5)
