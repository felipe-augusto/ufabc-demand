# -*- coding: utf-8 -*-

import json
from random import randint

ids_cursos_ufabc =  {
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

def open_data_from_quad(quad):
	with open('data/' + quad + '/prepared.json') as data_file:    
		data = json.load(data_file)
	return data

def transform_dict_to_array_and_sort(cursos_ids):
	cursos_ids_array = []
	for item in cursos_ids:
		cursos_ids_array.append(cursos_ids[item])
	cursos_ids_array.sort()
	return cursos_ids_array

cursos_ids_sorted_array = transform_dict_to_array_and_sort(ids_cursos_ufabc)

disciplina_data = []

def add_disciplina_data_to(current_array):
	global disciplina_data
	disciplina_data = current_array

# 1 = Santo Andre, 0 = Sao Bernardo
def add_campus_value(disciplina):
	global disciplina_data
	if disciplina['campus'].rfind('anto') != -1:
		disciplina_data.append(1)
	else:
		disciplina_data.append(0)

def add_cr_aluno_value(disciplina):
	global disciplina_data
	disciplina_data.append(disciplina['cr_aluno'])

def add_reprovacoes_value(disciplina):
	global disciplina_data
	disciplina_data.append(disciplina['reprovacoes'])

def add_vagas_value(disciplina):
	global disciplina_data
	disciplina_data.append(disciplina['vagas'])

def add_turno_value(disciplina):
	global disciplina_data
	if disciplina['turno'].rfind('not') != -1:
		disciplina_data.append(1)
	else:
		disciplina_data.append(0)

def add_cursos_obrigatorios_value(disciplina):
	global cursos_ids_sorted_array
	for obrigatoria in cursos_ids_sorted_array:
		if obrigatoria in disciplina['obrigatorias']:
			disciplina_data.append(1)
		else:
			disciplina_data.append(0)

def should_add_to_training_array():
	# one in twenty
	if randint(0,20) % 11 != 1:
		return True
	else:
		return False

def should_add_to_training_array_looking_for_best_error(amostras):
	if randint(0,758) < amostras:
		return True
	else:
		return False

def add_ratio_value(disciplina):
	return disciplina['ratio']