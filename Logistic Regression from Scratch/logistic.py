from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import numpy as np


class CustomLogisticRegression:

    def __init__(self, fit_intercept=True, l_rate=0.01, n_epoch=100):
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch
        bc_dataset = load_breast_cancer(as_frame=True)["frame"]
        X = bc_dataset.loc[:, ['worst concave points', 'worst perimeter', 'worst radius']]
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        y = bc_dataset["target"]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, train_size=0.8, random_state=43)
        self.coef_ = None
        self.mse_error = None
        self.log_error = None

    def sigmoid(self, t):
        return 1 / (1 + np.e ** (-t))

    def fit_mse(self, X_train, y_train):
        if self.fit_intercept:
            self.coef_ = np.zeros(X_train.shape[1] + 1)
        else:
            self.coef_ = np.zeros(X_train.shape[1])

        self.mse_error = []
        for _ in range(self.n_epoch):
            mse_error_step = []
            for i, row in enumerate(X_train):
                y_hat = self.predict_proba(row, self.coef_)
                mse_error_iter = ((y_hat - y_train.iloc[i]) ** 2) / len(y_train.values)
                mse_error_step.append(mse_error_iter)
                if self.fit_intercept:
                    self.coef_[0] -= self.l_rate * (y_hat - y_train.iloc[i]) * y_hat * (1 - y_hat)
                    for b in range(1, len(self.coef_)):
                        self.coef_[b] -= self.l_rate * (y_hat - y_train.iloc[i]) * y_hat * (1 - y_hat) * row[b - 1]
                else:
                    for b in range(len(self.coef_)):
                        self.coef_[b] -= self.l_rate * (y_hat - y_train.iloc[i]) * y_hat * (1 - y_hat) * row[b]
            self.mse_error.append(mse_error_step)

    def fit_log_loss(self, X_train, y_train):
        if self.fit_intercept:
            self.coef_ = np.zeros(X_train.shape[1] + 1)
        else:
            self.coef_ = np.zeros(X_train.shape[1])

        self.log_error = []
        for _ in range(self.n_epoch):
            log_error_step = []
            for i, row in enumerate(X_train):
                y_hat = self.predict_proba(row, self.coef_)
                log_error_iter = -(y_train.iloc[i] * np.log(y_hat)
                                   + (1 - y_train.iloc[i]) * np.log(1 - y_hat)) / len(y_train.values)
                log_error_step.append(log_error_iter)
                if self.fit_intercept:
                    self.coef_[0] -= (self.l_rate * (y_hat - y_train.iloc[i])) / len(X_train)
                    for b in range(1, len(self.coef_)):
                        self.coef_[b] -= (self.l_rate * (y_hat - y_train.iloc[i]) * row[b - 1]) / len(X_train)
                else:
                    for b in range(len(self.coef_)):
                        self.coef_[b] -= (self.l_rate * (y_hat - y_train.iloc[i]) * row[b]) / len(X_train)
            self.log_error.append(log_error_step)

    def predict_proba(self, row, coef_):
        if self.fit_intercept:
            t = np.dot(row, coef_[1:]) + coef_[0]
        else:
            t = np.dot(row, coef_)
        return self.sigmoid(t)

    def predict(self, X_test, cut_off=0.5):
        y_pred = np.ones(len(X_test))
        for i, row in enumerate(X_test):
            y_hat = self.predict_proba(row, self.coef_)
            if y_hat < cut_off:
                y_pred[i] = 0.0
        return y_pred


lr = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=1000)

lr.fit_mse(lr.X_train, lr.y_train)
y_predicted_mse = lr.predict(lr.X_test, cut_off=0.5)
acs_mse = accuracy_score(lr.y_test, y_predicted_mse)

lr.fit_log_loss(lr.X_train, lr.y_train)
y_predicted_log = lr.predict(lr.X_test, cut_off=0.5)
acs_log = accuracy_score(lr.y_test, y_predicted_log)

model = LogisticRegression()
model.fit(lr.X_train, lr.y_train)
y_predicted = model.predict(lr.X_test)
acs = accuracy_score(lr.y_test, y_predicted)

dictionary = dict()
dictionary['mse_accuracy'] = acs_mse
dictionary['logloss_accuracy'] = acs_log
dictionary['sklearn_accuracy'] = acs
dictionary['mse_error_first'] = lr.mse_error[0]
dictionary['mse_error_last'] = lr.mse_error[-1]
dictionary['logloss_error_first'] = lr.log_error[0]
dictionary['logloss_error_last'] = lr.log_error[-1]
print(dictionary)

print(f'{format(min(lr.mse_error[0]), ".5f")}')
print(f'{format(min(lr.mse_error[-1]), ".5f")}')
print(f'{max(lr.log_error[0]).round(5)}')
print(f'{max(lr.log_error[-1]).round(5)}')

