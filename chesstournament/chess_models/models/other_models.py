from django.db import models

class Referee(models.Model):
	# Referee name. Can be null or blanck
	name = models.CharField(max_length=128, null=True, blank=True)

	# Referee number assigned. Can be null or blank, and by default is -1
	