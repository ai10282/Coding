import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import GridSearchCV


def fit_predict_eval(model, features_train, features_test, target_train, target_test):
    model.fit(features_train, target_train)
    target_predicted = model.predict(features_test)
    score = round(accuracy_score(target_test, target_predicted), 4)
    print(f'Model: {model}\nAccuracy: {score}\n')
    return score


def fit_predict_eval_best(model, features_train, features_test, target_train, target_test):
    model.fit(features_train, target_train)
    target_predicted = model.predict(features_test)
    score = round(accuracy_score(target_test, target_predicted), 4)
    print(model.best_estimator_)
    return score


(x, y), (_, _) = tf.keras.datasets.mnist.load_data()
x = x.reshape(x.shape[0], x.shape[1] * x.shape[2])
normalizer = Normalizer()
x = normalizer.transform(x)
X_train, X_test, y_train, y_test = train_test_split(x[:6000], y[:6000], test_size=0.3, random_state=40)

dictionary = {'KNeighborsClassifier': fit_predict_eval(KNeighborsClassifier(), X_train, X_test, y_train, y_test),
              'DecisionTreeClassifier': fit_predict_eval(DecisionTreeClassifier(random_state=40), X_train, X_test,
                                                         y_train, y_test),
              'LogisticRegression': fit_predict_eval(LogisticRegression(solver="liblinear"), X_train, X_test, y_train,
                                                     y_test),
              'RandomForestClassifier': fit_predict_eval(RandomForestClassifier(random_state=40), X_train, X_test,
                                                         y_train, y_test)}

first_key_max = None
first_value_max = 0
second_key_max = None
second_value_max = 0
for i in range(2):
    if i == 0:
        for key in dictionary:
            if dictionary.get(key) == max(dictionary.values()):
                first_key_max = key
                first_value_max = dictionary.pop(key)
                break
    else:
        for key in dictionary:
            if dictionary.get(key) == max(dictionary.values()):
                second_key_max = key
                second_value_max = dictionary.get(key)
                break
dictionary[first_key_max] = first_value_max
print(f'Best: {first_key_max}-{first_value_max}, {second_key_max}-{second_value_max}')

argument_1 = {'n_neighbors': [3, 4], 'weights': ['uniform', 'distance'], 'algorithm': ['auto', 'brute']}
argument_2 = {'n_estimators': [300, 500],
              'max_features': ['auto', 'log2'], 'class_weight': ['balanced', 'balanced_subsample']}

model1 = GridSearchCV(KNeighborsClassifier(), param_grid=argument_1, scoring='accuracy', n_jobs=-1)
model2 = GridSearchCV(RandomForestClassifier(random_state=40), param_grid=argument_2, scoring='accuracy', n_jobs=-1)

print('K-nearest neighbours algorithm')
score1 = fit_predict_eval_best(model1, X_train, X_test, y_train, y_test)
print('accuracy:', score1)
print()
print('Random forest algorithm')
score2 = fit_predict_eval_best(model2, X_train, X_test, y_train, y_test)
print('accuracy:', score2)
