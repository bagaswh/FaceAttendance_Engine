from utils import Map

codes = Map({
    'reqintents': Map({
        'INTENT_REQ_FACE_ID': 0x1,
        'INTENT_REQ_FETCH_NEWLY_INSERTED_FACES_DATA': 0x2,
        'INTENT_REQ_ALL_FACES_DATA': 0x6,
        'INTENT_REQ_NEWLY_INSERTED_FACES_DATA': 0x7,
        'INTENT_REQ_UPDATE_FACES_DATA': 0x8
    }),

    'status': Map({
        'DONE': 0x0
    }),

    'dataformats': Map({
        'BINARY': 0x1,
        'STRING': 0x2,
        'MULTIPART': 0x4
    }),

    'sockettypes': Map({
        'REP': 0x1,
        'REQ': 0x2
    }),

    'operationtypes': Map({
        'SEND': 0x1,
        'REC': 0x2
    }),

    'socketstates': Map({
        'LISTENING': 0x1,
        'CYCLE_SENT': 0x2,
        'CYCLE_RECEIVED': 0x4,
        'CYCLE_DONE': 0x8,
        'IDLE': 0x16,
    })
})


addresses = Map({
    'REQ_ADDRESS_CONNECT': 'tcp://localhost:5556',
    'REP_ADDRESS_BIND': 'tcp://*:5555'
})
