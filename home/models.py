from django.db import models

# Create your models here.
class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStemp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self) -> str:
        return 'Message from ' + self.name
    

class CreatePost(models.Model):
    user_id=models.AutoField(primary_key= True)
    image=models.ImageField(upload_to='images/')
    title=models.CharField('Post Title',max_length=100)
    description=models.CharField('Post Description',max_length=1000)
    posted_date=models.DateField(auto_now_add=True, blank=True)
    name=models.CharField('Name',max_length=100)

