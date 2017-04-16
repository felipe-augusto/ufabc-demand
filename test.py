# -*- coding: utf-8 -*-
#!/usr/bin/env python -W ignore::DeprecationWarning

import json
from pprint import pprint
from sklearn import linear_model
from random import randint
clf = linear_model.LinearRegression()

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

quad = '1q2017'

cursos_ids = {
  'Bacharelado em Ciência da Computação': 16,
  'Bacharelado em Ciência e Tecnologia': 20,
  'Bacharelado em Ciências Biológicas': 17,
  'Bacharelado em Ciências Econômicas': 1,
  'Bacharelado em Ciências e Humanidades': 22,
  'Bacharelado em Filosofia': 10,
  'Bacharelado em Física': 28,
  'Bacharelado em Matemática': 21,
  'Bacharelado em Neurociência' : 24,
  'Bacharelado em Planejamento Territorial': 11,
  'Bacharelado em Políticas Públicas': 3,
  'Bacharelado em Química': 14,
  'Bacharelado em Relações Internacionais': 27,
  'Engenharia Aeroespacial': 26,
  'Engenharia Ambiental e Urbana': 6,
  'Engenharia Biomédica': 18,
  'Engenharia de Energia': 7,
  'Engenharia de Gestão': 23,
  'Engenharia de Informação' : 8,
  'Engenharia de Instrumentação, Automação e Robótica': 2,
  'Engenharia de Materiais': 15,
  'Licenciatura em Ciências Biológicas': 13,
  'Licenciatura em Física': 25,
  'Licenciatura em Matemática': 9,
  'Licenciatura em Química': 4
}

def transform_dict_to_array(cursos_ids):
	cursos_ids_array = []
	for item in cursos_ids:
		cursos_ids_array.append(cursos_ids[item])
	return cursos_ids_array

# as the length is 25, we need at least 25 attributes just for the courses !!
cursos_ids_array = transform_dict_to_array(cursos_ids)
cursos_ids_array.sort()
# len(cursos_ids_array)

with open('data/' + quad + '/prepared.json') as data_file:    
	   data = json.load(data_file)

x = []
y = []

tests = []

for index, item in enumerate(data):
	global test_me
	array_of_datas = []
	# [campus, cr_aluno, reprovacoes, vagas]

	# first argument is campus -> 1 = Santo Andre, 0 = Sao Bernardo
	if data[item]['campus'].rfind('anto') != -1:
		array_of_datas.append(1)
	else:
		array_of_datas.append(0)
	# second argument is cr aluno
	array_of_datas.append(data[item]['cr_aluno'])
	# third arguemnt reprovacoes
	array_of_datas.append(data[item]['reprovacoes'])
	# fouth argument vagas
	array_of_datas.append(data[item]['vagas'])
	# fifth argument turno -> 1 = noturno, 0 = diurno
	if data[item]['turno'].rfind('not') != -1:
		array_of_datas.append(1)
	else:
		array_of_datas.append(0)

	# cursos, abrindo em diversos parametros
	for obrigatoria in cursos_ids_array:
		if obrigatoria in data[item]['obrigatorias']:
			array_of_datas.append(1)
		else:
			array_of_datas.append(0)
	
	if randint(0,12) % 5 != 1:
		y.append(data[item]['ratio'])
		x.append(array_of_datas)
	else:
		tests.append([array_of_datas, data[item]['ratio']])

clf.fit(x, y);

print 'tamanho do vetor de treinamento: ', len(x)
print 'tamanho do vetor de testes: ', len(tests)

for index, test in enumerate(tests):
	if index > 20:
		break
	print 'previsao: ', clf.predict(test[0])[0], '- real: ', test[1]