from django.db import models

from django.db import models

class UserData(models.Model):
    Input = models.CharField(max_length=100)
    QRCodeImage = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.Input




class Register(models.Model):
    Name=models.CharField(max_length=50)
    User_ID=models.CharField(max_length=50)
    Email=models.EmailField(max_length=50)
    Mobile=models.BigIntegerField()
    Address=models.CharField(max_length=60)
    Password1=models.CharField(max_length=50)
    Password2=models.CharField(max_length=50)
