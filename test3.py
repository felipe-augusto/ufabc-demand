# -*- coding: utf-8 -*-
#!/usr/bin/env python -W ignore::DeprecationWarning
import time
import json
from pprint import pprint
from sklearn import linear_model
import utils
import warnings
from sklearn.preprocessing import PolynomialFeatures

warnings.filterwarnings("ignore", category=DeprecationWarning)
clf = linear_model.LinearRegression()

disciplinas = utils.open_data_from_quad('1q2017')
min_error = 1

# fill training_array, test_array and expected_y_outputs
ini = time.time()
print 'Processando...Aguarde...'
for number in range(1,758):
	training_array = []
	test_array = []
	expected_y_outputs = []
	for index, i in enumerate(disciplinas):
		current_disciplina = disciplinas[i]
		# we need to transform disciplinas inputs to an array
		current_disciplina_array = []

		# set where inputs will be added
		utils.add_disciplina_data_to(current_disciplina_array)
		# add inputs
		utils.add_campus_value(current_disciplina)
		utils.add_cr_aluno_value(current_disciplina)
		utils.add_reprovacoes_value(current_disciplina)
		utils.add_vagas_value(current_disciplina)
		utils.add_turno_value(current_disciplina)
		utils.add_cursos_obrigatorios_value(current_disciplina)

		# add desired output
		current_y = utils.add_ratio_value(current_disciplina)

		# choose between test or training data and append
		if utils.should_add_to_training_array_looking_for_best_error(number):
			training_array.append(current_disciplina_array)
			expected_y_outputs.append(current_y)
		else:
			current_test = [current_disciplina_array, current_y]
			test_array.append(current_test)

	# train
	poly = PolynomialFeatures(degree=1)
	training_array_changed = poly.fit_transform(training_array)
	clf.fit(training_array, expected_y_outputs);

	# number of wrong requisicoes that we are willing to accept
	threshold = 10
	error = 0

	for index, test in enumerate(test_array):
		input = test[0]
		vagas = input[3]
		predicao_requisicoes = vagas * clf.predict(input)[0] #poly.fit_transform(input)
		requisicoes = vagas * test[1]
		if abs(predicao_requisicoes - requisicoes) > threshold:
			error += 1

	error_percentage = float(error) / len(test_array)
	if error_percentage < min_error:
		min_error = error_percentage
		min_error_training_size = len(training_array)	
		min_error_test_size = len(test_array)
fim = time.time()
print "Tempo Total de Execução: ", fim-ini, ' segundos'
print min_error
print 'tamanho do vetor de treinamento com menor erro: ', min_error_training_size
print 'tamanho do vetor de testes com menor erro: ', min_error_test_size