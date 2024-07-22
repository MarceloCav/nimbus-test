from django.db import models

class ReceivedData(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, unique=True)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.email} - {self.phone} - {self.age}'
