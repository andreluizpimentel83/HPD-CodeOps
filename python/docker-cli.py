#!/usr/bin/venv python3.6.5

############################################# EXERCICIO PYTHON #######################################
# 1. Melhorar o script adicionando docstrings e controlando as exceptions			     #
# 2. Criar mais uma função, agora para remover containers que estão "bindando" alguma porta no host  #
# 3. Criar o argumento para a linha de comando							     #
######################################################################################################

import docker
from datetime import datetime

def logando(mensagem, e, logfile='docker-cli.log'):
	data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
	with open('docker-cli.log', 'a') as log:
		texto = "%s \t %s \t %s \n" % (data_atual, mensagem, str(e))
		log.write(texto)

def createContainer(args):
	"""Criar container utilizando a imagem de sua preferencia e caso desejado, executando tambem um comando no container"""
	try:
		client = docker.from_env()
		executando = client.containers.run(args.image, args.command, detach=True)
		print("O container ID %s foi criado com sucesso!" %(executando.short_id))
		return(executando)
	except docker.errors.ImageNotFound as e:
		logando("Erro: Imagem nao encontrada!\nPara mais informacoes verifique o registro de log 'docker-cli.log' e/ou utilize, <comando> -h", e)
	except docker.errors.NotFound as e:
		logando("Erro: Comando nao encontrado!\nPara mais informacoes verifique o registro de log 'docker-cli.log' e/ou utilize, <comando> -h", e)
	except Exception as e:
		logando("Erro: Favor verificar o comando digitado.\nPara mais informacoes verifique tambem o registro de log 'docker-cli.log' e/ou utilize, <comando> -h", e)
	finally:
		print("Metodo 'Metodo 'createContainer()' executado!\n")

def listInfoContainers(args):
	"""Listar informacoes relevantes de containers em execucao"""
	try:
		client = docker.from_env()
		list_containers = client.containers.list()
		for cada_container in list_containers:
			connecting = client.containers.get(cada_container.id)
			dicionario = connecting.attrs['HostConfig']['PortBindings']
			lista = dicionario.get('80/tcp')
			if lista == None:
				print("Container ID: %s \nImage: %s \nHost BIND: None \nCommand: %s \nVolumes: %s \n" %(connecting.short_id, connecting.attrs['Config']['Image'], connecting.attrs['Config']['Cmd'], connecting.attrs['Config']['Volumes']))
			else:
				porta = lista[0].get('HostPort')
				print("Container ID: %s \nImage: %s \nIP: %s \nHost BIND: %s \nCommand: %s \nVolumes: %s \n" %(connecting.short_id, connecting.attrs['Config']['Image'], connecting.attrs['NetworkSettings']['IPAddress'], porta, connecting.attrs['Config']['Cmd'], connecting.attrs['Config']['Volumes']))
	except docker.errors.NotFound as e:
		logando("Erro: Comando nao encontrado!\nPara mais informacoes verifique o registro de log 'docker-cli.log' e/ou utilize, <comando> -h", e)
	except Exception as e:
		logando("Erro: Favor verificar o comando digitado.\nPara mais informacoes verifique tambem o registro de log 'docker-cli.log' e/ou utilize, <comando> -h", e)
	finally:
		print("Metodo 'listInfoContainers()' executado!\n")

def findContainer(args):
	"""Procurar containers em execucao com a imagem desejada"""
	try:
		client = docker.from_env()
		list_containers = client.containers.list()
		for cada_container in list_containers:
			conectando = client.containers.get(cada_container.id)
			imagem_container = cada_container.attrs['Config']['Image']
			if str(args.image).lower() in str(imagem_container).lower():
				print("O container ID %s utiliza a imagem %s e contem a palavra %s em seu nome." % (cada_container.short_id, cada_container.attrs['Config']['Image'], args.image))
			else:
				print("O container ID %s utiliza a imagem %s e nao contem a palavra %s em seu nome." % (cada_container.short_id, cada_container.attrs['Config']['Image'], args.image))
	except docker.errors.NotFound as e:
		logando("Erro: Comando nao encontrado!\nPara mais informacoes verifique o registro de log 'docker-cli.log' e/ou utilize, <comando> -h", e)
	except Exception as e:
		logando("Erro: Favor verificar o comando digitado.\nPara mais informacoes verifique tambem o registro de log 'docker-cli.log' e/ou utilize, <comando> -h", e)
	finally:
		print("Metodo 'Metodo 'findContainer()' executado!\n")

def removeContainerWithBindingPort(args):
	"""Remover containers que estao bindando alguma porta no host"""
	try:
		client = docker.from_env()
		list_containers = client.containers.list()
		for cada_container in list_containers:
			connecting = client.containers.get(cada_container.id)
			imagem_container = connecting.attrs['Config']['Image']
			dicionario = connecting.attrs['HostConfig']['PortBindings']
			if isinstance(dicionario,dict):
				for chave,valor in dicionario.items():
					valor = str(valor)
					porta = ''.join(filter(str.isdigit, valor))
					print("ContainerID: %s \nHost Port BIND: %s \nRemovendo o container %s do docker...\n" %(connecting.short_id, porta, connecting.short_id))
					connecting.stop()
					connecting.remove()
	except docker.errors.NotFound as e:
		logando("Erro: Comando nao encontrado!\nPara mais informacoes verifique o registro de log 'docker-cli.log' e/ou utilize, <comando> -h", e)
	except Exception as e:
		logando("Erro: Favor verificar o comando digitado.\nPara mais informacoes verifique tambem o registro de log 'docker-cli.log' e/ou utilize, <comando> -h", e)
	finally:
		print("Metodo 'removeContainerWithBindingPort()' executado!\n")

parser = argparse.ArgumentParser(description="Meu exercicio da aula de python FODASTICA do HPD.")
subparser = parser.add_subparsers()

criando_container = subparser.add_parser('create')
criando_container.add_argument('--image', required=True, help="nome da imagem a ser criada", type=str)
criando_container.add_argument('--command', required=False, help="comando a ser executado no container", type=str)
criando_container.set_defaults(func=createContainer)

list_cont = subparser.add_parser('ls')
list_cont.set_defaults(func=listInfoContainers)

procurar_container = subparser.add_parser('find')
procurar_container.add_argument('--image', required=False, help="nome da imagem a procurar", type=str)
procurar_container.set_defaults(func=findContainer)

remover_container = subparser.add_parser('remove')
#remover_container.add_argument('--all-bind', required=False, type=str)
remover_container.set_defaults(func=removeContainerWithBindingPort)

cmd = parser.parse_args()
cmd.func(cmd)
