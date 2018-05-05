#!/usr/bin/venv python3.6

import docker
import argparse

def removeContainerWithBindingPort(args):
	"""Removendo containers que estao bindando alguma porta no host..."""
	try:
		client = docker.from_env()
		list_containers = client.containers.list()
		for cada_container in list_containers:
			connecting = client.containers.get(cada_container.id)
			imagem_container = connecting.attrs['Config']['Image']
			dicionario = connecting.attrs['HostConfig']['PortBindings']
			lista = dicionario.get('80/tcp')
			if lista == None:
				print("O container ID %s nao esta bindando porta no host." %(connecting.short_id))
			else:
				lista = dicionario.get('80/tcp')
				porta = lista[0].get('HostPort')
				print("O container ID %s esta bindando a porta %s no host.\nRemovendo o %s do docker.." %(connecting.short_id, porta, connecting.short_id))
				connecting.stop()
				connecting.remove()	
				print("Container ID %s removidoi do docker!" %(connecting.short_id))
	except docker.errors.NotFound as e:
		logando("Erro: Comando nao encontrado!\nPara mais informacoes verifique o registro de log 'docker-cli.log' e/ou utilize, <comando> -h", e)
	except Exception as e:
		logando("Erro: Favor verificar o comando digitado.\nPara mais informacoes verifique tambem o registro de log 'docker-cli.log' e/ou utilize, <comando> -h", e)
	finally:
		print("Metodo 'removeContainerWithBindingPort()' executado!\n")

parser = argparse.ArgumentParser(description="Meu CLI docker FODAO feito durante a aula e persolanizado pos aula.")
subparser = parser.add_subparsers()

procurar_container = subparser.add_parser('remove')
#procurar_container.add_argument('--all-bind', required=False)
procurar_container.set_defaults(func=removeContainerWithBindingPort)

cmd = parser.parse_args()
cmd.func(cmd)
