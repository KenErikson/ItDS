from math import sqrt

import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np

###
# Import the boston dataset into separate train/test AND input/result arrays
# (13+1 columns for every row - 404 rows in train data - 102 rows in test data)
#
# x_train:
#  0: CRIM: Per capita crime rate by town
#  1: ZN: Proportion of residential land zoned for lots over 25,000 sq. ft
#  2: INDUS: Proportion of non-retail business acres per town
#  3: CHAS: Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
#  4: NOX: Nitric oxide concentration (parts per 10 million)
#  5: RM: Average number of rooms per dwelling
#  6: AGE: Proportion of owner-occupied units built prior to 1940
#  7: DIS: Weighted distances to five Boston employment centers
#  8: RAD: Index of accessibility to radial highways
#  9: TAX: Full-value property tax rate per $10,000
# 10: PTRATIO: Pupil-teacher ratio by town
# 11: B: 1000(Bk — 0.63)², where Bk is the proportion of [people of African American descent] by town
# 12: LSTAT: Percentage of lower status of the population
#
# y_train:
# MEDV: Median value of owner-occupied homes in $1000s
###
from tensorflow.python.keras._impl.keras.wrappers.scikit_learn import KerasRegressor

(x_train, y_train), (x_test, y_test) = keras.datasets.boston_housing.load_data()

###
# Describe dataset
###
print("The train input is a tuple of shape: "+str(x_train.shape))
print("The train output is an array of length: "+str(len(y_train)))

median_value_array = y_train
plt.title("Overview of mean value in dataset")
plt.xlabel("Median value of Home (k$)")
plt.ylabel("Nr of occurences in test data")
plt.hist(median_value_array)
plt.show()

crim_rate = np.array(x_train[:,0])
plt.title("Value/Crime Rate")
plt.xlabel("Crime Rate (per town capita)")
plt.ylabel("Median value of Home (k$)")
plt.scatter(crim_rate,median_value_array,linestyle = 'None')
plt.show()

average_number_of_rooms = np.array(x_train[:,5])
plt.title("Value/Number of rooms")
plt.xlabel("Average number of rooms")
plt.ylabel("Median value of Home (k$)")
plt.scatter(average_number_of_rooms,median_value_array,linestyle = 'None')
plt.show()

###
# Initiate Model
###
model = keras.Sequential()
model.add(keras.layers.Dense(9, activation=tf.nn.relu,kernel_initializer='normal', input_shape=(13,)))
#model.add(keras.layers.Dropout(0.2)) # Not Overfitting data
model.add(keras.layers.Dense(11, kernel_initializer='normal', activation=tf.nn.relu))
model.add(keras.layers.Dense(1, kernel_initializer='normal'))
model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='mean_squared_error')

###
# Train Model
# (Fit model to training data set)
###
model.fit(x_train, y_train, epochs=2000, verbose=0)

###
# Test Model
# (get mean squared error of test data in k$)
###
mean_squared_error = model.evaluate(x_test, y_test)
print("Mean squared error on test data: "+str(round(mean_squared_error,2))+"k$")
print("Mean error on test data: "+str(round(sqrt(mean_squared_error),2))+"k$")