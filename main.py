import base64
import json
import cv2

from facerecognizer import FaceRecognizer
import image
from constants import codes
import messaging

reqintents = codes.reqintents


def get_all_faces_data():
    messaging.send(messaging.req, codes.dataformats.MULTIPART, [
        [reqintents.INTENT_REQ_ALL_FACES_DATA], b''])

    json_faces_data = messaging.receive(
        messaging.req, codes.dataformats.STRING)
    faces_data = json.loads(json_faces_data)

    return faces_data


def load_images(faces_data):
    labels = []
    faces = []
    for face_data in faces_data:
        labels.append(face_data['user_id'])

        imagedata = image.b64decode(face_data['image_base64'])
        faces.append(imagedata)

    print('adding faces data...')
    FaceRecognizer.add_faces(labels, faces)
    print('done adding faces data!')


def update_faces_data(socket, faces_data):
    faces_data = json.loads(faces_data)

    load_images(faces_data)
    messaging.send(socket, codes.dataformats.BINARY, bytearray([0x0]))


def sendfaceid(socket, image_base64):
    imagedata = image.b64decode(image_base64)
    rgb_small_frame = image.get_rgb_small_frame(imagedata)

    face_locations, ids, face_landmarks = FaceRecognizer.recognize(
        rgb_small_frame)
    jsonstring = json.dumps({
        'face_locations': face_locations,
        'ids': ids
    })

    messaging.send(socket, codes.dataformats.STRING, jsonstring)
    # socket.send_string(jsonstring)


def register_intent_handlers():
    messaging.on(reqintents.INTENT_REQ_FACE_ID, sendfaceid)
    messaging.on(reqintents.INTENT_REQ_UPDATE_FACES_DATA,
                 update_faces_data)


def main():
    load_images(get_all_faces_data())

    register_intent_handlers()

    print('Listening message...')
    messaging.listen()


if __name__ == '__main__':
    main()
