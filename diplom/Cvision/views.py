from django.shortcuts import render
from .models import Inquiry,Person,Model,Result
from django.db import connection
from django.shortcuts import redirect
from django.views.generic import View
from .forms import *
import face_recognition
import cv2
import subprocess
from django.core.files.storage import FileSystemStorage
import numpy as np
from .tasks import Video_analisis
import json
from datetime import date

# Create your views here.
def index(request):
    return render(request,'Cvision/main.html')

def history(request):
    inquiry = Inquiry.objects.all()
    context = {
        'inquiry': inquiry,
    }

    return render(request,'Cvision/HistorySearch.html',context)

def work(request):
    return render(request,'Cvision/WorkObl.html')

def record(request, id):
    inquiry = Inquiry.objects.get(id=id)
    record = Result.objects.all().filter(inquiry_id=id)

    context = {
        'record':record,
        'inquiry': inquiry,
    }
    return render(request,'Cvision/Records.html',context)

def cabinet_adm(request):
    person = Person.objects.all()
    form = PersonForm();
    context = {
        'person': person,
        'form': form
    }
    return render(request,'Cvision/CabAdm.html',context)

class delete_person(View):
    def get(self, request, id):
        person = Person.objects.all().filter(id=id)
        return render(request,'Cvision/delete_person',context = {'person':person})

    def post(self, request, id):
        person = Person.objects.all().filter(id=id)
        person.delete()
        return redirect('/Cvision/cabinet_adm')

class create_person(View):

    def post(self, request, id_admin):
        new_person = Person()
        new_person.admin_id = id_admin

        new_person.Full_name = request.POST.get("NAME")
        new_person.Description = request.POST.get("DESCRIPTION")
        new_person.save()
        return redirect('/Cvision/cabinet_adm')

class create_model(View):

    def post(self, request, id_person, id_user):
        new_model = Model()

        image = face_recognition.load_image_file(request.FILES['myfile'])
        lists = face_recognition.face_encodings(image)[0].tolist()
        new_model.Encoding = json.dumps(lists)
        new_model.Description = request.POST.get("DESCRIPTION")
        new_model.FileName = request.FILES['myfile']
        new_model.person_id = id_person
        new_model.DateAdded = date.today()
        new_model.NameEmployee_id = id_user
        new_model.save()
        return redirect('/Cvision/cabinet_adm/person/'+str(id_person))

class delete_model(View):

    def post(self, request, id_model):
        model = Model.objects.all().filter(id=id_model)
        model.delete()
        return redirect(request.META.get('HTTP_REFERER'))


def result(request, id):
    inquiry = Inquiry.objects.get(id=id)
    results = Result.objects.all().filter(inquiry_id=id)

    context = {
        'results':results,
        'inquiry': inquiry,
    }
    return render(request,'Cvision/Result.html',context)


class video_analysis(View):
    def post(self, request, id_user):
        filename = request.POST.get("VIDEO")
        new_inquiry = Inquiry()
        new_inquiry.Date = date.today()
        new_inquiry.Name_video = filename
        new_inquiry.employee_id = id_user
        new_inquiry.save()
        result = Video_analisis.delay(filename, new_inquiry.id)
        return render(request,'Cvision/WorkObl.html', context={'result': result, 'id': new_inquiry.id})



def photo_person(request, id):
    models = Model.objects.all().filter(person_id=id)
    persons = Person.objects.all().filter(id=id)
    context = {
        'models': models,
        'person': persons,
        'id_person': id,
    }
    return render(request, 'Cvision/PhotosPerson.html', context)

