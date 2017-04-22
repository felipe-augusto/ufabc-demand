import json
import pandas
from pprint import pprint
from sklearn import linear_model
import utils
import warnings
from sklearn.preprocessing import PolynomialFeatures

# load training data
dataframe = pandas.read_csv("data/training.csv", delim_whitespace=True, header=None)
dataset = dataframe.values

number_of_inputs = 29

X = dataset[:,0:number_of_inputs]
Y = dataset[:,number_of_inputs]

# load test data
dataframe = pandas.read_csv("data/test.csv", delim_whitespace=True, header=None)
dataset = dataframe.values

X_test = dataset[:,0:number_of_inputs]
Y_test = dataset[:,number_of_inputs]

print 'Tamanho do vetor de treinamento: ', len(X)
print 'Tamanho do vetor de testes: ', len(X_test)

clf = linear_model.LinearRegression()
poly = PolynomialFeatures(degree=1)
X_poly = poly.fit_transform(X)
clf.fit(X_poly, Y);

X_test_poly = poly.fit_transform(X_test)
results = clf.predict(X_test_poly)
score = clf.score(X_test_poly, Y_test)

print "Your score is: ", score

error_sum = 0.0
for i, result in enumerate(results):
	error_sum += abs(result - Y_test[i])**2

print "Your MSE is: ", error_sum / len(X_test)