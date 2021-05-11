
from diplom.celery import app
from multiprocessing import current_process
import face_recognition
import cv2
import subprocess
from .models import Person,Model,Result
import numpy as np
import json
from django.shortcuts import redirect
import datetime
import time
from celery_progress.backend import ProgressRecorder
from celery import shared_task

def get_frame_types(video_fn):
    command = 'ffprobe -v error -show_entries frame=pict_type  -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [video_fn]).decode()
    frame_types = out.replace('pict_type=', '').split()
    return zip(range(len(frame_types)), frame_types)




@shared_task(bind=True)
def Video_analisis(self ,filename, id):
    progress_recorder = ProgressRecorder(self)


    persons = Person.objects.all()

    frame_types = get_frame_types(filename)
    p_frames = [x[0] for x in frame_types if x[1] == 'I']

    input_movie = cv2.VideoCapture(filename)
    fps = input_movie.get(cv2.CAP_PROP_FPS)
    id_person = []
    known_faces = []
    persona_models = []
    for person in persons:
        models = Model.objects.all().filter(person_id=person.id)
        for model in models:
            json_model = json.loads(model.Encoding)
            persona_models.append(np.array(json_model))
        id_person.append(person.id)
        known_faces.append(persona_models)
        persona_models = []
        print(id_person)

    frames = []
    frame_count = 0


    print("Считывание")
    for frame_no in p_frames:
        input_movie = cv2.VideoCapture(filename)
        print("Всего кадров {}".format(len(p_frames)))
        frame_count += 1
        progress_recorder.set_progress(frame_count, len(p_frames)) #для прогресс бара
        print("_читает кадр {}".format(frame_count))
        input_movie.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        #print("__получает кадр ")
        ret, frame = input_movie.read()
        print(ret)
        if not ret:
            print("пропуск")
        else:
            #print("___resize ")
            frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
            #print("____rgb ")
            rgb_frame = frame[:, :, ::-1]

            frames.append(rgb_frame)

        if len(frames) == 16:
            print("____находим все лица ")
            batch_of_face_locations = face_recognition.batch_face_locations(frames, number_of_times_to_upsample=0)
            for frame_number_in_batch, face_locations in enumerate(batch_of_face_locations):
                number_of_faces_in_frame = len(face_locations)
                frame_number = frame_count - 16 + frame_number_in_batch
                print("I found {} face(s) in frame #{}.".format(number_of_faces_in_frame, frame_number))
                face_encodings = face_recognition.face_encodings(frames[frame_number_in_batch], face_locations)
                for face_encoding in face_encodings:
                    index = 0
                    for known_face in known_faces:
                        print("_____находим личности ")
                        match = face_recognition.compare_faces(known_face, face_encoding, tolerance=0.50)
                        print(match)
                        for identity_found in match:
                            if(identity_found):
                                new_result = Result()

                                Seconds_all = int(p_frames[frame_number-1]/fps)
                                hours, remainder = divmod(Seconds_all, 3600)
                                minutes, seconds = divmod(remainder, 60)
                                string_time = str(hours)+":"+str(minutes)+":"+str(seconds)
                                new_result.DateTime = string_time

                                new_result.person_id = id_person[index]
                                new_result.inquiry_id = id

                                new_result.save()
                                break

                        index += 1
            frames = []
    return "Done"




