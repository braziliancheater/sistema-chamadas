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
import threading

known_face_encodings = []
known_face_names = []

presenca_registrada = {}  # Dicionário para manter o status de presença de cada pessoa
stop_video_feed = False
status = '0'  # Inicialmente, o status é '0'
last_face_detected_time = time.time()

def update_status():
    global status
    while not stop_video_feed:
        try:
            response = requests.get('http://localhost:5001/obter_status')
            if response.status_code == 200:
                status = response.text
            else:
                status = '0'
        except Exception as e:
            status = '0'
        time.sleep(2)  # Atualiza o status a cada 2 segundos

def start_status_thread():
    status_thread = threading.Thread(target=update_status)
    status_thread.daemon = True
    status_thread.start()

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
    time.sleep(2)  # espera 2 segundos para parar o feed de vídeo
    try:
        known_face_encodings, known_face_names = load_known_faces()
    except Exception as e:
        log.log_erro(__name__, f"erro ao carregar as faces: {e}")
    stop_video_feed = False

def gen_frames():
    global last_face_detected_time
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    frame_count = 0

    while True:
        if stop_video_feed:
            break

        success, frame = video_capture.read()
        if not success:
            break
        else:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

            faces_detected = False

            if process_this_frame:
                if frame_count % 2 == 0 and status == '1':
                    face_locations = face_recognition.face_locations(small_frame)
                    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                    if face_encodings:
                        faces_detected = True
                        last_face_detected_time = time.time()

                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        name = "Desconhecido"
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        if True in matches:
                            best_match_index = np.argmin(face_distances)
                            name = known_face_names[best_match_index]

                            # Atualiza o status de presença para "registrado"
                            presenca_registrada[name] = "Presença registrada"
                        else:
                            # Atualiza o status de presença para "não registrado"
                            presenca_registrada[name] = "Presença não registrada"

            # Desenha um quadrado no meio da tela para indicar a presença se houver uma face detectada recentemente
            height, width, _ = frame.shape
            current_time = time.time()

            if faces_detected or current_time - last_face_detected_time <= 5:
                for name, presence_status in presenca_registrada.items():
                    text = f"Reconhecido: {name} | {presence_status}"
                    font = cv2.FONT_HERSHEY_DUPLEX
                    font_scale = 0.8
                    thickness = 1
                    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)

                    # Calcular a posição do quadrado centralizado
                    text_width, text_height = text_size
                    box_x = (width - text_width) // 2 - 10
                    box_y = (height + text_height) // 2 + 100
                    box_width = text_width + 20
                    box_height = text_height + 20

                    # Desenhar o fundo do texto
                    color = (0, 255, 0) if presence_status == "Presença registrada" else (0, 0, 255)
                    cv2.rectangle(frame, (box_x, box_y - text_height - 10), (box_x + box_width, box_y + 10), color, cv2.FILLED)

                    # Desenhar o texto centralizado
                    cv2.putText(frame, text, (box_x + 10, box_y - 5), font, font_scale, (255, 255, 255), thickness)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        frame_count += 1
        process_this_frame = not process_this_frame

    video_capture.release()

@index.route('/obter_usuarios')
def obter_usuarios():
    global presenca_registrada
    if presenca_registrada is None:
        return 'Nenhum usuário detectado', 200
    else:
        return presenca_registrada, 200

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
    start_status_thread()
    usuarios = Usuarios.query.all()
    valor = Propriedades.query.filter_by(prop_nome='status').first()
    
    if not valor:
        log.log_aviso(__name__, "Propriedade status não encontrada, criando.")
        valor = Propriedades(prop_nome='status', prop_valor='0')
        db.session.add(valor)
        db.session.commit()
        time.sleep(2)
    
    status_text = f'Chamada em andamento | Prop: {valor.prop_valor}' if valor.prop_valor == '1' else f'Aguardando chamada | Prop: {valor.prop_valor}'
    return render_template('index/index.html', status=status_text, usuarios=usuarios)
