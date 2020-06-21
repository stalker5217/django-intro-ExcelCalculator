from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length = 20)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length = 100)
    # email 인증 여부
    user_validate = models.BooleanField(default=False)