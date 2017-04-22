# follow this tutorial
# http://machinelearningmastery.com/regression-tutorial-keras-deep-learning-library-python/

import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import utils

# load training data
dataframe = pandas.read_csv("data/training.csv", delim_whitespace=True, header=None)
dataset = dataframe.values

number_of_inputs = 30

X = dataset[:,0:number_of_inputs]
Y = dataset[:,number_of_inputs]

# load test data
dataframe = pandas.read_csv("data/test.csv", delim_whitespace=True, header=None)
dataset = dataframe.values

X_test = dataset[:,0:number_of_inputs]
Y_test = dataset[:,number_of_inputs]

print 'Tamanho do vetor de treinamento: ', len(X)
print 'Tamanho do vetor de testes: ', len(X_test)

# define base model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(30, input_dim=30, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model

# evaluate model with standardized dataset
seed = 7
numpy.random.seed(seed)
estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', KerasRegressor(build_fn=baseline_model, epochs=50, batch_size=5, verbose=0)))
pipeline = Pipeline(estimators)

# 10-fold cross validation
kfold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(pipeline, X, Y, cv=kfold)
print("Standardized: %.2f (%.2f) MSE" % (results.mean(), results.std()))

# training model
pipeline.fit(X,Y)

score = pipeline.score(X_test, Y_test)
print "Your score is", score

error_sum = 0.0
right = 0
thresold = 10

for i, result in enumerate(results):
	vagas = int(X_test[i][3])
	requisicoes_previstas = (int) (vagas * result)
	requisicoes_reais = (int) (vagas * Y_test[i])
	print utils.right_or_wrong(requisicoes_previstas,
				requisicoes_reais,
				thresold), "|",\
			"requisicoes previstas:", requisicoes_previstas, "-", \
			requisicoes_reais, "reais"
			
	if abs(requisicoes_previstas - requisicoes_reais) < thresold:
		right += 1;
	error_sum += abs(result - Y_test[i])**2

print "You got", right, "right from", len(X_test), "(" ,float(right) / len(X_test), ")%"
print "Your MSE is: ", error_sum / len(X_test)