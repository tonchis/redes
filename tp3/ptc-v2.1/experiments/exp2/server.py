# -*- coding: utf-8 -*-

##########################################################
#                 Trabajo Práctico 3                     #
#         Programación de protocolos end-to-end          #
#                                                        #
#              Teoría de las Comunicaciones              #
#                       FCEN - UBA                       #
#              Segundo cuatrimestre de 2014              #
##########################################################


try:
    from ptc import Socket
except:
    import sys
    sys.path.append('../../')
    from ptc import Socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
MESSAGE = 'inadsuiuhsasjjaoijswoioiwe' * 1000
MESSAGE_SIZE = 100

received = str()

# Usar sockets PTC dentro de bloques with. Esto nos asegura que los recursos
# subyacentes serán liberados de forma adecuada una vez que el socket ya no
# se necesite.
with Socket(2,0.1) as server_sock:
    # Ligar el socket a una interfaz local a través de la tupla (IP, PORT).
    server_sock.bind((SERVER_IP, SERVER_PORT))
    # Pasar al estado LISTEN.
    server_sock.listen()
    # Esta llamada se bloqueará hasta que otro PTC intente conectarse. No
    # obstante, luego de diez segundos de no recibir conexiones, PTC se
    # dará por vencido.
    server_sock.accept()
    message_received = ''
    while len(message_received) < len(MESSAGE):
        message_received += server_sock.recv(MESSAGE_SIZE)
