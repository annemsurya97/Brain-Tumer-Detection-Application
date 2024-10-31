from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Test_data(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='Test/')
    output=models.TextField()
    date=models.DateField(auto_now=True)
    time=models.TimeField(auto_now=True)
    