from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
	title = models.CharField(max_length = 255)

	def __str__(self):
		return 'Category ' + str(self.title)


class Subcategory(models.Model):
	title = models.CharField(max_length = 255)

	category = models.ForeignKey(Category, on_delete = models.CASCADE)

	def __str__(self):
		return 'Subcategory ' + str(self.title) + ' of ' + str(self.category)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)

	name = models.CharField(max_length = 255)

	phone_number = models.CharField(max_length = 255)

	def __str__(self):
		return 'Profile of ' + str(self.user)





class Offer(models.Model):
	title = models.CharField(max_length = 255)

	category = models.ForeignKey(Category, on_delete = models.CASCADE)

	subcategory = models.ForeignKey(Subcategory, on_delete = models.CASCADE)

	price = models.PositiveIntegerField()

	description = models.TextField()

	user = models.ForeignKey(Profile, on_delete = models.CASCADE)

	
	def description_short(self):
		text = str(self.description)
		if len(text) < 200:
			return text
		else:
			return text[:200]


	def __str__(self):
		return 'Offer ' + str(self.title)


class OfferImage(models.Model):
	offer = models.ForeignKey(Offer, on_delete = models.CASCADE)
	image = models.ImageField(upload_to = 'images/')
