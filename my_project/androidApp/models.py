from django.db import models

# Create your models here.
class Location(models.Model):
	name = models.CharField('Location', unique=True, max_length=100)
	
	def __str__(self):
		return self.name

class Data(models.Model):
	location = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)
	routeId = models.CharField('Id', max_length=3, null=True, unique=True)
	text = models.CharField('Route', max_length=200)
	
	def __str__(self):
		return self.location.name + " " +self.routeId

class Route(models.Model):
	path = models.CharField('Route', max_length=200)
	
	def __str__(self):
		return self.path
