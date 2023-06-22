import pandas as pd
import os
import requests
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder


def clean_data(path):
    df = pd.read_csv(path)
    df['b_day'] = pd.to_datetime(df['b_day'], format='%m/%d/%y')
    df['draft_year'] = pd.to_datetime('01/01/' + df['draft_year'].astype('string'), format='%m/%d/%Y')
    df['team'].fillna('No Team', inplace=True)
    df['height'] = df['height'].str.split(' / ').apply(lambda x: x[1]).astype('float')
    df['weight'] = df['weight'].str.split(' / ').apply(lambda x: x[1]).str.replace(' kg.', '').astype('float')
    df['country'] = df['country'].str.replace('^((?!USA).)*$', 'Not-USA', regex=True)
    df['draft_round'] = df['draft_round'].str.replace('Undrafted', '0')
    df['salary'] = df['salary'].str.replace('$', '').astype('float')
    return df


def feature_data(df):
    df['version'] = pd.to_datetime(df['version'].str.replace('k', '0').str.lstrip('NBA'))
    df.insert(0, 'age', (df['version'].dt.strftime('%Y').astype('int') - df['b_day'].dt.strftime('%Y').astype('int')))
    df.insert(1, 'experience',
              (df['version'].dt.strftime('%Y').astype('int') - df['draft_year'].dt.strftime('%Y').astype('int')))
    df.insert(2, 'bmi', (df['weight'] / df['height'] ** 2))
    df.drop(['version', 'b_day', 'draft_year', 'weight', 'height'], axis=1, inplace=True)
    df.drop(['full_name', 'jersey', 'college', 'draft_peak'], axis=1, inplace=True)
    return df


def multicol_data(df):
    # df.drop(['position', 'team', 'country', 'draft_round'], axis=1, inplace=True)
    df_corr = df.corr(method='pearson', numeric_only=True)
    df.drop(['age'], axis=1, inplace=True)
    return df


def transform_data(df):
    X = df.drop(['salary'], axis=1)
    y = df['salary']
    num_feat_df = X.select_dtypes('number')
    scaler = StandardScaler()
    num_feat_df = scaler.fit_transform(num_feat_df).tolist()
    column_values = ['experience', 'bmi', 'rating']
    num_feat_df = pd.DataFrame(data=num_feat_df, columns=column_values)
    num_feat_df = num_feat_df.iloc[:, [2, 0, 1]]
    cat_feat_df = X.select_dtypes('object')
    encoder = OneHotEncoder()
    cat_feat_df = encoder.fit_transform(cat_feat_df).toarray()
    column_values = np.concatenate(encoder.categories_).ravel().tolist()
    cat_feat_df = pd.DataFrame(data=cat_feat_df, columns=column_values)
    X = pd.concat([num_feat_df, cat_feat_df], axis=1)
    return X, y


if not os.path.exists('../Data'):
    os.mkdir('../Data')

if 'nba2k-full.csv' not in os.listdir('../Data'):
    print('Train dataset loading.')
    url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/nba2k-full.csv', 'wb').write(r.content)
    print('Loaded.')

data_path = "../Data/nba2k-full.csv"
df_cleaned = clean_data(data_path)
df_featured = feature_data(df_cleaned)
df = multicol_data(df_featured)
X, y = transform_data(df)

printing = {
    'shape': [X.shape, y.shape],
    'features': list(X.columns),
    }
print(printing)