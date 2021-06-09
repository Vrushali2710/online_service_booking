import uuid
from django.db import models


class user(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    username = models.CharField(max_length=200,)
    password = models. 



# Create your models here.
