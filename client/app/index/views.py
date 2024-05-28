import cv2
import face_recognition
import numpy as np
from . import index
from app import db, log
from ..tabelas import Usuarios, Imagens, Propriedades
import base64
from io import BytesIO
from PIL import Image
import time
import requests
from flask import render_template, Response

known_face_encodings = []
known_face_names = []
presencas_registras = []
stop_video_feed = False

def load_known_faces():
    global known_face_encodings, known_face_names
    known_face_encodings.clear()
    known_face_names.clear()

    users = Usuarios.query.all()

    for user in users:
        user_images = Imagens.query.filter_by(id_usuario=user.id).all()
        for user_image in user_images:
            try:
                base64_image = user_image.imagem.split(",")[-1]
                img_data = base64.b64decode(base64_image)
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
    log.log_sucesso(__name__, "iniciando Faces")
    global known_face_encodings, known_face_names, stop_video_feed
    stop_video_feed = True
    time.sleep(2)  # Wait for 2 seconds to ensure the video feed is stopped
    try:
        known_face_encodings, known_face_names = load_known_faces()
    except Exception as e:
        log.log_erro(__name__, f"erro ao carregar as faces: {e}")
    stop_video_feed = False
def gen_frames():
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True  # Processa apenas um frame a cada 2 frames para economizar tempo de processamento
    frame_count = 0  # Contador de frames
    while True:
        if stop_video_feed:
            break

        success, frame = video_capture.read()
        if not success:
            break
        else:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # converte em rgb
            small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)  # diminui a resolução da imagem para 1/4

            # Processa o frame apenas se o contador indicar
            if process_this_frame:
                # Reduz o processamento realizando-o apenas a cada 2 frames
                if frame_count % 2 == 0:
                    face_locations = face_recognition.face_locations(small_frame)
                    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        name = "Unknown"
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        if True in matches:
                            best_match_index = np.argmin(face_distances)
                            name = known_face_names[best_match_index]

                            status_presenca = requests.get('http://localhost:5001/obter_status').text
                            if status_presenca == '1' and name not in presencas_registras:
                                presencas_registras.append(name)
                                status = requests.get(f'http://localhost:5001/presencas/registrar/{name}')
                                if status.status_code == 200:
                                    log.log_sucesso(__name__, f"Presença registrada: {name}")
                                else:
                                    log.log_erro(__name__, f"Erro ao registrar presença: {name}")

                        cv2.putText(frame, name, (left + 6, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        frame_count += 1  # Incrementa o contador de frames
        process_this_frame = not process_this_frame  # Alterna o processamento do frame

    video_capture.release()

@index.route('/obter_status')
def obter_status():
    try:
        propriedades = Propriedades.query.filter_by(prop_nome='status').first()
        valor = propriedades.prop_valor
        return valor, 200
    except Exception as e:
        log.log_erro(__name__, f"erro ao obter o status: {e}")
        return '0', 500

@index.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@index.route('/')
def index():
    init_known_faces()
    usuarios = Usuarios.query.all()
    valor = Propriedades.query.filter_by(prop_nome='status').first()
    if valor.prop_valor is None:
        log.log_aviso(__name__, "Propriedade status não encontrada, criando.")
        valor = '0'
        prop = Propriedades(prop_nome='status', prop_valor=valor)
        db.session.add(prop)
        db.session.commit()
        time.sleep(2)
    status = f'Chamada em andamento | Prop: {valor.prop_valor}' if valor.prop_valor == '1' else f'Aguardando chamada | Prop: {valor.prop_valor}'
    return render_template('index/index.html', status=status, usuarios=usuarios)
