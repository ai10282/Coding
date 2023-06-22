import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


class CustomLinearRegression:

    def __init__(self, *, fit_intercept):
        self.fit_intercept = fit_intercept
        self.coefficient = np.array([])
        self.intercept = 0.0

    def fit(self, X, y):
        if self.fit_intercept:
            one = np.ones(np.size(f1)).reshape(-1, 1)
            X = np.append(one, X, axis=1)
            beta = np.linalg.solve(np.dot(np.transpose(X), X), np.dot(np.transpose(X), y))
            self.coefficient = beta[1:]
            self.intercept = beta[0]
        else:
            self.coefficient = np.linalg.solve(np.dot(np.transpose(X), X), np.dot(np.transpose(X), y))

    def predict(self, X):
        return np.dot(X, self.coefficient) + self.intercept

    def r2_score(self, y, yhat):
        return 1 - (np.sum((y - yhat) ** 2) / np.sum((y - np.mean(y)) ** 2))

    def rmse(self, y, yhat):
        return np.sqrt(np.sum((y - yhat) ** 2) / np.size(y))


if __name__ == "__main__":
    f1 = [2.31, 7.07, 7.07, 2.18, 2.18, 2.18, 7.87, 7.87, 7.87, 7.87]
    f2 = [65.2, 78.9, 61.1, 45.8, 54.2, 58.7, 96.1, 100.0, 85.9, 94.3]
    f3 = [15.3, 17.8, 17.8, 18.7, 18.7, 18.7, 15.2, 15.2, 15.2, 15.2]
    y = [24.0, 21.6, 34.7, 33.4, 36.2, 28.7, 27.1, 16.5, 18.9, 15.0]
    X = np.stack((f1, f2, f3), axis=1)
    regCustom = CustomLinearRegression(fit_intercept=True)
    regCustom.fit(X, y)
    pred_y = regCustom.predict(X)
    r2 = regCustom.r2_score(np.array(y), pred_y)
    rmse = regCustom.rmse(np.array(y), pred_y)

    regSci = LinearRegression(fit_intercept=True)
    regSci.fit(X, y)
    y_train = regSci.predict(X)
    rmse_train = np.sqrt(mean_squared_error(y, y_train))
    r2_train = r2_score(y, y_train)

    data_dict = {'Intercept': regCustom.intercept - regSci.intercept_,
                 'Coefficient': regCustom.coefficient - regSci.coef_,
                 'R2': r2 - r2_train,
                 'RMSE': rmse - rmse_train}
    print(data_dict)
