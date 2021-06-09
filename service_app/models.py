import uuid
from django.db import models


class admin(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    username = models.CharField(max_length=200,)



# Create your models here.
