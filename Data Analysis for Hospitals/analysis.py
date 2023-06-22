import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 8)

general = pd.read_csv('test/general.csv')
prenatal = pd.read_csv('test/prenatal.csv')
sport = pd.read_csv('test/sports.csv')

prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)
sport.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'}, inplace=True)

data = pd.concat([general, prenatal, sport], ignore_index=True)
data.drop('Unnamed: 0', axis=1, inplace=True)
data.dropna(how='all', inplace=True)
data['gender'] = data['gender'].replace(['woman', 'female'], 'f')
data['gender'] = data['gender'].replace(['man', 'male'], 'm')
data['gender'].fillna('f', inplace=True)
data[['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']] = \
    data[['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']].fillna(0)

data.plot(y='age', kind='hist', bins=5)
plt.show()
pie_chart = data['diagnosis'].value_counts()
plt.pie(pie_chart, labels=pie_chart.index, autopct='%1.1f%%')
plt.show()
plt.violinplot(data.height)
plt.show()
