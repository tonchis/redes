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
    from ptc import Socket, SHUT_WR
except:
    import sys
    sys.path.append('../../')
    from ptc import Socket, SHUT_WR

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
CLOCK_TICK = 0.01
TRANSFER_DATA = 'abcdefghijklmnopqrstuvwxyz' * 1000
TRANSFER_CHUNK_SIZE = 100
# Usar sockets PTC dentro de bloques with. Esto nos asegura que los recursos
# subyacentes serán liberados de forma adecuada una vez que el socket ya no
# se necesite.
# Seteo alpha y beta de la linea de comandos
alpha = float(sys.argv[1])
beta = float(sys.argv[2])
with Socket() as client_sock:
    # Establecer una conexión al PTC corriendo en el puerto SERVER_PORT en
    # el host con dirección SERVER_IP. Esta llamada es bloqueante, aunque
    # en este caso se declara un timeout de 10 segundos. Pasado este tiempo,
    # el protocolo se dará por vencido y la conexión no se establecerá.
    client_sock.connect((SERVER_IP, SERVER_PORT))
    # Una vez aquí, la conexión queda establecida exitosamente. Podemos enviar
    # y recibir datos arbitrarios.
    client_sock.protocol.rto_estimator.alpha = alpha
    client_sock.protocol.rto_estimator.beta = beta
    data_index = 0
    while data_index < len(TRANSFER_DATA):
        chunk_size = min(len(TRANSFER_DATA) - data_index, TRANSFER_CHUNK_SIZE)
        chunk = TRANSFER_DATA[data_index : data_index + chunk_size]
        client_sock.send(chunk)
        data_index = data_index + chunk_size
    #client_sock.shutdown(SHUT_WR)