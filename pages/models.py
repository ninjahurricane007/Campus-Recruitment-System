from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    ph_num = models.TextField(max_length=10)
    clg_name = models.CharField(max_length=50)
    sem = models.CharField(max_length=10)
    brch = models.TextField()
    cgpa= models.TextField()
    bklgs= models.TextField()
    dp_img = models.ImageField(null=True,blank=True,upload_to="images/")
    isCordinator = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

