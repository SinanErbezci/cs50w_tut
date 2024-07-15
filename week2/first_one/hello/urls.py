from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sinan", views.sinan, name="sinan"),
    path("<str:name>", views.greet, name="greet")
    # any string with name parameter. Name is going to be that path.
    
]