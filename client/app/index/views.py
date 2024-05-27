from flask import render_template, Response
import cv2
import face_recognition
import numpy as np
from . import index
from app import db, log
from ..tabelas import Usuarios, Imagens, Propriedades
import base64
from io import BytesIO
from PIL import Image

def load_known_faces():
    known_face_encodings = []
    known_face_names = []
    
    # busca todos os usuarios
    users = Usuarios.query.all()
    
    for user in users:
        # obtem todas as imagens de usuarios
        user_images = Imagens.query.filter_by(id_usuario=user.id).all()
        for user_image in user_images:
            try:
                # obtem as imagens em divide na ,
                base64_image = user_image.imagem.split(",")[-1]
                
                # decode do base64 para imagem
                img_data = base64.b64decode(base64_image)
                
                # carrega as imagens e encode do face_recognition
                img = Image.open(BytesIO(img_data))
                img_array = np.array(img)
                face_encodings = face_recognition.face_encodings(img_array)
                if face_encodings:
                    known_face_encodings.append(face_encodings[0])
                    known_face_names.append(user.nome)
                    log.log_sucesso(__name__, f"usuario {user.nome} carregado.")
            except Exception as e:
                log.log_erro(__name__, f"erro ao carregar a imagem do usuario: {user.nome}: {e}")
    
    return known_face_encodings, known_face_names

def init_known_faces():
    # inicia o processo de carregamento das faces
    log.log_sucesso(__name__, "iniciando Faces")
    global known_face_encodings, known_face_names
    known_face_encodings, known_face_names = load_known_faces()

def gen_frames():
    # inicializa a captura de video
    video_capture = cv2.VideoCapture(0)
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Não Reconhecido"
                color = (0, 0, 255)  # vermelho para desconhecido

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                if face_distances.size > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        color = (0, 255, 0)  # verde para conhecido

                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                cv2.putText(frame, name, (left + 6, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video_capture.release()

@index.route('/video_feed')
def video_feed():
    # retorna a resposta com o video
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@index.route('/')
def index():
    # inicializa o sistema de faces
    init_known_faces()

    # obtem o status
    try:
        pass
    except:
        pass

    return render_template('index/index.html', status='True')