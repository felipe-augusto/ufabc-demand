import json

quad = '1q2017'

new_cursos_ids = {
  73 : 16,
  76 : 20,
  72 : 17,
  60 :  1,
  78 : 22,
  66 : 10,
  84 : 28,
  77 : 21,
  80 : 24,
  67 : 11,
  58 :  3,
  70 : 14,
  83 : 27,
  82 : 26,
  61 :  6,
  74 : 18,
  62 :  7,
  79 : 23,
  64 :  8,
  57 :  2,
  71 : 15,
  69 : 13,
  81 : 25,
  63 :  9,
  59 :  4
}

def read_requisicoes():
	global quad

	with open(quad + '/requisicoes.json') as data_file:    
	    data = json.load(data_file)

	requisicoes = {}

	for user in data[0]:
		for matricula in data[0][user]:
			if matricula in requisicoes.keys():
				requisicoes[matricula] += 1
			else:
				requisicoes[matricula] = 1

	return requisicoes

def create_hash(nome):
	disciplina = nome.split("-")[0]
	turma = disciplina[disciplina.rfind(" "):].replace(" ", "");
	disciplina = disciplina[0:disciplina.rfind(" ")]
	turno = nome.split("(");
	campus = turno[1].replace(")", "").split('|')[0];

	if (turno[0].rfind('atutino') != -1):
		turno = "diurno"
	elif (turno[0].rfind('oturno') != -1):
		turno = "noturno"
	return disciplina + '@' + turma + '@' + turno + '@' + campus

def read_todas_disciplinas():
	global quad

	with open(quad + '/todas_disciplinas.json') as data_file:    
	    data = json.load(data_file)

	disciplinas = {}

	for disciplina in data:
		disciplinas[disciplina['id']] = disciplina

	return disciplinas

def read_disciplinas():
	global quad

	with open(quad + '/disciplinas.json') as data_file:    
	    data = json.load(data_file)

	return data

requisicoes = read_requisicoes()
todas_disciplinas = read_todas_disciplinas()

hashable = {}

for disciplina in todas_disciplinas:
	tmp_hash = create_hash(todas_disciplinas[disciplina]['nome'])
	hashable[tmp_hash] = todas_disciplinas[disciplina]

disciplinas = read_disciplinas()

prepared_data = {}

for index, disciplina in enumerate(disciplinas):
	tmp_hash = disciplina['disciplina'] + '@' + disciplina['turma'] + '@' + disciplina['turno'] + '@' + disciplina['campus'].replace(" do Campo", "")
	if tmp_hash in hashable:
		current_disciplina = hashable[tmp_hash]['id']
		prepared_data[current_disciplina] = {}
		prepared_data[current_disciplina]['obrigatorias'] = []
		for obrigatoria in hashable[tmp_hash]['obrigatoriedades']:
			if obrigatoria['curso_id'] in new_cursos_ids.keys():
				curso_id = new_cursos_ids[obrigatoria['curso_id']]
			else:
				curso_id = obrigatoria['curso_id']
			
			prepared_data[current_disciplina]['obrigatorias'].append(curso_id)
		
		prepared_data[current_disciplina]['campus'] = disciplina['campus']
		prepared_data[current_disciplina]['vagas'] = hashable[tmp_hash]['vagas']

		prepared_data[current_disciplina]['turno'] = disciplina['turno']

		# print hashable[tmp_hash]
		divider = 0
		cr_aluno = 0
		reprovacoes = 0
		if 'teoria_help' in disciplina:
			reprovacoes = int(disciplina['teoria_help']['reprovacoes'].replace('%', ''))
			cr_aluno += float(disciplina['teoria_help']['cr_aluno'])
			divider += 1
		if 'pratica_help' in disciplina:
			reprovacoes = int(disciplina['pratica_help']['reprovacoes'].replace('%', ''))
			cr_aluno += float(disciplina['pratica_help']['cr_aluno'])
			divider += 1
		if divider != 0:
			prepared_data[current_disciplina]['cr_aluno'] =  cr_aluno / divider
			prepared_data[current_disciplina]['reprovacoes'] = reprovacoes / divider
		else:
			prepared_data.pop(current_disciplina, None)

		if current_disciplina in prepared_data:
			if str(hashable[tmp_hash]['id']) in requisicoes:
				prepared_data[current_disciplina]['ratio'] = float(requisicoes[str(hashable[tmp_hash]['id'])]) / float(hashable[tmp_hash]['vagas'])
			else:
				prepared_data.pop(current_disciplina, None)

with open(quad + '/prepared.json', 'w') as fp:
    json.dump(prepared_data, fp)