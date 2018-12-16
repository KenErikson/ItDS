import tensorflow as tf
from tensorflow import keras

###
# Import the boston data set into separate train/test AND input/output arrays
# (13 columns for every input - 404 rows in train data - 102 rows in test data)
###
(x_train, y_train), (x_test, y_test) = keras.datasets.boston_housing.load_data()

###
# Initiate Model
###
model = keras.Sequential()
model.add(keras.layers.Dense(13, activation=tf.nn.relu,kernel_initializer='normal', input_shape=(13,)))
#model.add(keras.layers.Dense(128, activation=tf.nn.relu))
#model.add(keras.layers.Dense(6, kernel_initializer='normal', activation='relu'))
model.add(keras.layers.Dense(1, kernel_initializer='normal'))
model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='mean_squared_error')

###
# Train Model
# (Fit model to training data set)
###
model.fit(x_train, y_train, epochs=100)

###
# Test Model
# (get mean squared error of test data in k$)
###
mean_squared_error = model.evaluate(x_test, y_test)
#scores = model.evaluate(x_train, y_train)
print("Mean squared error of test data: "+str(mean_squared_error)+"k$")