from django.contrib import admin

from .models import Inquiry,Person,Model,Result

admin.site.register(Inquiry)
admin.site.register(Person)
admin.site.register(Model)
admin.site.register(Result)