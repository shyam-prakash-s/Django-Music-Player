from django.db import models

# Create your models here.
class Song(models.Model):
    title= models.TextField()
    artist= models.TextField()
    image= models.ImageField()
    audio_file = models.FileField(blank=True,null=True)
    audio_link = models.CharField(max_length=200,blank=True,null=True)
    duration=models.CharField(max_length=20)

    def __str__(self):
        return self.title #,self.id
    


class Artist(models.Model):
    name= models.TextField()
    image= models.ImageField()

    def __str__(self):
        return self.name #,self.id