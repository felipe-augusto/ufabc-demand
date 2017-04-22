# -*- coding: utf-8 -*-
#!/usr/bin/env python -W ignore::DeprecationWarning

import json
from pprint import pprint
from sklearn import linear_model
import utils
import warnings
from sklearn.preprocessing import PolynomialFeatures

warnings.filterwarnings("ignore", category=DeprecationWarning)
clf = linear_model.LinearRegression()

disciplinasq1 = utils.open_data_from_quad('1q2017')
disciplinasq2 = utils.open_data_from_quad('2q2017')

training_array = []
test_array = []
expected_y_outputs = []

# start output csv
training_csv = utils.start_csv('training');
test_csv = utils.start_csv('test');

def add_to_csv(disciplinas):
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
		# utils.add_vagas_value(current_disciplina)
		utils.add_turno_value(current_disciplina)
		utils.add_cursos_obrigatorios_value(current_disciplina)

		# add desired output
		current_y = utils.add_ratio_value(current_disciplina)

		# choose between test or training data and append
		if utils.should_add_to_training_array():
			utils.add_line_to_csv(current_disciplina_array, current_y, training_csv)
			training_array.append(current_disciplina_array)
			expected_y_outputs.append(current_y)
		else:
			current_test = [current_disciplina_array, current_y]
			test_array.append(current_test)
			utils.add_line_to_csv(current_disciplina_array, current_y, test_csv)

add_to_csv(disciplinasq1)
add_to_csv(disciplinasq2)