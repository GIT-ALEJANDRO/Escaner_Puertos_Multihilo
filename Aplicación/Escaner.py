#!/usr/bin/env python3


import concurrent.futures
import socket


# Rango de puertos a escanear
RANGO_PUERTOS = (1, 65535)


# Función que devuelve el puerto y servicio si está abierto, None si está cerrado
def escanear_puerto(host, puerto):
	
	try:
		with socket.create_connection((host, puerto), timeout=1) as conexion:
			try:
				servicio = socket.getservbyport(puerto)
			except Exception:
				servicio = 'Desconocido'
			return puerto, servicio
	except Exception:
		pass
	
	
# Función que escanea los puertos con multihilo 
def escanear_puertos(host):
	
	puertos_abiertos = []
	
	with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
		futuros = {executor.submit(escanear_puerto, host, puerto): puerto for puerto in range(*RANGO_PUERTOS)}
		for futuro in concurrent.futures.as_completed(futuros):
			resultado = futuro.result()
			if resultado:
				puerto, servicio = resultado
				print(f'[*] Puerto: {puerto} Servicio: {servicio}')
				puertos_abiertos.append((puerto, servicio))
	return puertos_abiertos


def main():
	hosts = ['127.0.0.1']
	
	for host in hosts:
		print("------------------------------")
		print("   Escaner Local de Puertos   ")
		print("------------------------------")
		puertos_abiertos = escanear_puertos(host)
		
		if not puertos_abiertos:
			print('[!] No se encontraron puertos abiertos')
		
		
if __name__ == '__main__':
	try:
		main()
	except Exception as e:
			print(e)
			exit(1)
		
	