import zmq

import utils
from constants import codes, addresses

# ZeroMQ connection initialization
__context = zmq.Context()

# Recognition Engine -> NodeJS
req = __context.socket(zmq.REQ)
req.connect(addresses.REQ_ADDRESS_CONNECT)

# Recognition Engine <- .NET code
rep = __context.socket(zmq.REP)
rep.bind(addresses.REP_ADDRESS_BIND)

# function handlers for intent
intent_handlers = {}
for reqintent in codes.reqintents:
    intent_handlers[codes.reqintents[reqintent]] = []

repsocketstate = codes.socketstates.IDLE
reqsocketstate = codes.socketstates.IDLE


def on(intent_code, handler):
    if not utils.isfunction(handler):
        return

    if intent_code in intent_handlers:
        intent_handlers[intent_code].append(handler)


def route_intent(socket, intent_code, message_body):
    print(f'Received message with intent code {intent_code}')
    if intent_code in intent_handlers:
        for handler in intent_handlers[intent_code]:
            handler(socket, message_body)
    else:
        send(rep, codes.dataformats.STRING, str(codes.status.DONE))


def receive(socket, format):
    message = ''
    if format == codes.dataformats.BINARY:
        message = socket.recv()
    elif format == codes.dataformats.STRING:
        message = socket.recv_string()
    elif format == codes.dataformats.MULTIPART:
        message = socket.recv_multipart()
    else:
        return

    return message


def send(socket, format, message, onreply=None):
    if format == codes.dataformats.BINARY:
        socket.send(message)
    elif format == codes.dataformats.STRING:
        socket.send_string(message)
    elif format == codes.dataformats.MULTIPART:
        socket.send_multipart([bytearray(message[0]), message[1]])
    else:
        return


def listen():
    repsocketstate = codes.socketstates.LISTENING
    while True:
        recval = receive(rep, codes.dataformats.MULTIPART)
        repsocketstate = codes.socketstates.CYCLE_RECEIVED

        intent = recval[0][0]
        message_body = recval[1]

        with open('debug_output.txt', 'w') as f:
            print(message_body, file=f)

        route_intent(rep, intent, message_body)
