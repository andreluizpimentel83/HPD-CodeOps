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

parser = argparse.ArgumentParser(prog='python docker-cli.py', description="Meu CLI docker FODAO feito durante a aula e persolanizado pos aula.", usage='%(prog)s [options]')
subparser = parser.add_subparsers()

procurar_container = subparser.add_parser('remove')
procurar_container.add_argument('--bind', required=False)
procurar_container.set_defaults(func=removeContainerWithBindingPort)

cmd = parser.parse_args()
cmd.func(cmd)
