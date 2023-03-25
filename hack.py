import argparse

import socket

parser = argparse.ArgumentParser()
parser.add_argument('ip_address')
parser.add_argument('port')
parser.add_argument('message')
args = parser.parse_args()

with socket.socket() as client_socket:
    client_socket.connect((args.ip_address, int(args.port)))
    message = args.message.encode()
    client_socket.send(message)
    buf_size = 1024
    response = client_socket.recv(buf_size)
    print(response.decode())
