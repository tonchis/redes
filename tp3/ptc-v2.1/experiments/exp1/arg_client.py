# -*- coding: utf-8 -*-

##########################################################
#                 Trabajo Práctico 3                     #
#         Programación de protocolos end-to-end          #
#                                                        #
#              Teoría de las Comunicaciones              #
#                       FCEN - UBA                       #
#              Segundo cuatrimestre de 2014              #
##########################################################

import sys
try:
    from ptc import Socket, SHUT_WR
except:
    sys.path.append('../../')
    from ptc import Socket, SHUT_WR

if len(sys.argv) == 1:
    print '\nUsage:\nsudo python arg_client.py ALPHA BETA\n'
    print 'To use default values, run:\nsudo python client.py\n'
    print 'Or manually use ALPHA = 0.125 and BETA = 0.25\n'
    exit()

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
CLOCK_TICK = 0.01

# Seteo alpha y beta de la linea de comandos
ALPHA = sys.argv[1]
BETA = sys.argv[2]

# Creo el arcihvo donde va el output
filename = "./results/A_" + str(ALPHA).replace('.',',') + "-B_" + str(BETA).replace('.',',') + ".txt"
f = open(filename, 'w')

to_send = 'a'
received = str()
import pdb

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
        line = str(i) + "\t" + str(client_sock.protocol.rto_estimator.rtt*CLOCK_TICK)\
               + "\t" + str(client_sock.protocol.rto_estimator.rto*CLOCK_TICK)
        print line
        f.write(line + '\n')
        i = i+1

    client_sock.shutdown(SHUT_WR)
    f.close()
    exit()
