import os
import requests

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error as mape

if not os.path.exists('../Data'):
    os.mkdir('../Data')

if 'data.csv' not in os.listdir('../Data'):
    url = "https://www.dropbox.com/s/3cml50uv7zm46ly/data.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/data.csv', 'wb').write(r.content)

data = pd.read_csv('../Data/data.csv')
X = data.drop(['salary'], axis=1)
df_corr = X.corr(method='pearson', numeric_only=True)
# print(df_corr)
X = X.drop(['experience', 'age'], axis=1)
y = data['salary']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)
lin_reg = LinearRegression(fit_intercept=True)
lin_reg.fit(X_train, y_train)
y_predicted = lin_reg.predict(X_test)
y_predicted[y_predicted < 0] = 0
mape_calc = mape(y_test, y_predicted)
print(mape_calc.round(5))
