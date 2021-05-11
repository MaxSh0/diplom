from django.db import models
from datetime import  date
from django.contrib.auth.models import User



class Inquiry(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    Date = models.DateField(default=date.today())
    Name_video = models.CharField(max_length=1500, verbose_name='name_video', null=True)


class Person(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Full_name = models.CharField(max_length=1500, verbose_name='full_name')
    Description = models.CharField(max_length=1500, verbose_name='description')
    Date = models.DateField(default=date.today())

    def __str__(self):
        return self.Full_name

class Model(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    Encoding = models.JSONField()
    Description = models.CharField(max_length=1500, verbose_name='description', default="Описание отсутствует")
    FileName = models.CharField(max_length=1500, verbose_name='filename', default="Имя файла отсутствует")
    DateAdded = models.DateField(default=date.today())
    NameEmployee = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.Encoding

class Result(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE)
    DateTime = models.TimeField()