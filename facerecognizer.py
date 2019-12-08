import numpy as np
import face_recognition

from utils import islist, isndarray


class FaceRecognizer:
    labels = []
    encodings = []

    @staticmethod
    def add_faces(labels, images):
        if not islist(labels):
            labels = [labels]
        if not islist(images) or isndarray(images):
            images = [images]

        for label, image in zip(labels, images):
            if isinstance(image, str):
                image = face_recognition.load_image_file(image)

            loaded_encoding = face_recognition.face_encodings(image)
            if len(loaded_encoding) > 0:
                FaceRecognizer.labels.append(label)
                FaceRecognizer.encodings.append(loaded_encoding[0])

    @staticmethod
    def recognize(image):
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                FaceRecognizer.encodings, face_encoding)

            name = ''

            face_distances = face_recognition.face_distance(
                FaceRecognizer.encodings, face_encoding)

            if (len(face_distances) > 0):
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = FaceRecognizer.labels[best_match_index]

                face_names.append(name)

        face_landmarks_list = face_recognition.face_landmarks(
            image, face_locations)

        return face_locations, face_names, face_landmarks_list
