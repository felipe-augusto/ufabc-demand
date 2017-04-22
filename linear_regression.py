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

clf = linear_model.HuberRegressor()
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
clf.fit(X_poly, Y);

X_test_poly = poly.fit_transform(X_test)
results = clf.predict(X_test_poly)
score = clf.score(X_test_poly, Y_test)

print "Your score is: ", score

error_sum = 0.0
right = 0
thresold = 10
total = 0
other_right = 0

for i, result in enumerate(results):
	vagas = int(X_test[i][3])
	requisicoes_previstas = (int) (vagas * result)
	requisicoes_reais = (int) (vagas * Y_test[i])

	print utils.right_or_wrong(requisicoes_previstas,
				requisicoes_reais,
				thresold), "|",\
			"requisicoes previstas:", requisicoes_previstas, "-", \
			requisicoes_reais, "reais"
	
	if(requisicoes_previstas > vagas):		
		total += 1
		if requisicoes_reais > vagas:
			other_right += 1
	if abs(requisicoes_previstas - requisicoes_reais) < thresold:
		right += 1;
	error_sum += abs(result - Y_test[i])**2

print "You got", right, "right from", len(X_test), "(" ,float(right) / len(X_test), ")%"
print "Correctly guess if more requisicoes then vagas: ", float(other_right) / total * 100, "%"
print "Your MSE is: ", error_sum / len(X_test)