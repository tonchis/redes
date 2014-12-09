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
MESSAGE = 'inadsuiuhsasjjaoijswoioiwe' * 1000
MESSAGE_SIZE = 100
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
    i = 0
    while i < len(MESSAGE):
        message_size = min(len(MESSAGE) - i, MESSAGE_SIZE)
        message = MESSAGE[i : i + message_size]
        i = i + message_size
        client_sock.send(message)
    #client_sock.shutdown(SHUT_WR)