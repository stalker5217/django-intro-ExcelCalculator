from django.urls import path
from . import views

urlpatterns = [
	# mapping 'email/send/'
	path('send', views.send, name='email_send')
]