from django.db import models
# from .tournament import Tournament

class Round(models.Model):
	# Round name.
	name = models.CharField(max_length=128, null=False, blank=False)

	# Tournament reference
	tournament = models.ForeignKey(to='chess_models.Tournament', null=False, blank=False, on_delete=models.CASCADE)

	# Round start date and hour. Can be null
	start_date = models.DateTimeField(auto_now_add=True, null=True)

	# Round end time
	end_date = models.DateTimeField(null=True)

	# Bool to check if the round has finished
	finish = models.BooleanField(default=False)
