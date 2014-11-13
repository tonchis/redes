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

to_send = 'a'
received = str()

# Usar sockets PTC dentro de bloques with. Esto nos asegura que los recursos
# subyacentes serán liberados de forma adecuada una vez que el socket ya no
# se necesite.
with Socket() as client_sock:
    # Establecer una conexión al PTC corriendo en el puerto SERVER_PORT en
    # el host con dirección SERVER_IP. Esta llamada es bloqueante, aunque
    # en este caso se declara un timeout de 10 segundos. Pasado este tiempo,
    # el protocolo se dará por vencido y la conexión no se establecerá.
    client_sock.connect((SERVER_IP, SERVER_PORT))
    # Una vez aquí, la conexión queda establecida exitosamente. Podemos enviar
    # y recibir datos arbitrarios.
    i = 0
    while i < 100:
        
        client_sock.send(to_send)
        #espero a que llegue el ack?
        client_sock.recv(10)
        #print i, " ", (client_sock.protocol.ticks-client_sock.protocol.rto_estimator.rtt_start_time)*CLOCK_TICK, " ", client_sock.protocol.rto_estimator.rto*CLOCK_TICK
        print i, " ", client_sock.protocol.rto_estimator.rtt*CLOCK_TICK, " ", client_sock.protocol.rto_estimator.rto*CLOCK_TICK
        i = i+1

    client_sock.shutdown(SHUT_WR)