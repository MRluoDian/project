from django.db import models

# Create your models here.


class Press(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)



class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    press = models.ForeignKey(to=Press,on_delete=models.CASCADE)

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    books= models.ManyToManyField(to='Book')