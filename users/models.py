from django.contrib.auth.models import models, AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
