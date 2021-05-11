from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('work', views.work, name ='work'),
    path('cabinet_adm/create_person/<int:id_admin>', views.create_person.as_view(), name='create_person'),
    path('cabinet_adm/person/create_model/<int:id_person>/<int:id_user>', views.create_model.as_view(), name='create_model'),
    path('cabinet_adm', views.cabinet_adm, name ='cabinet_adm'),
    path('history', views.history, name ='history'),
    path('record/<str:id>', views.record, name ='record'),
    path('result/<str:id>', views.result, name ='result'),

    path('cabinet_adm/person/<str:id>', views.photo_person, name="photo_person"),
    path('cabinet_adm/delete_person/<int:id>', views.delete_person.as_view(), name="delete_person"),
    path('cabinet_adm/delete_person_photo/<int:id_model>', views.delete_model.as_view(), name="delete_person_photo"),
    path('work/video_analysis/<int:id_user>', views.video_analysis.as_view(), name="video_analysis"),


]