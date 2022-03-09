from django.urls import path
from . import views



urlpatterns = [
    path('<int:problem_pk>', views.check)
    
]
