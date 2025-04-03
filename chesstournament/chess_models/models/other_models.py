from django.db import models


class Referee(models.Model):
    # Referee name. Can be null or blanck
    name = models.CharField(max_length=128, null=True, blank=True)

    # Referee number assigned. Can be null or blank, and by default is -1
    refereeNumber = models.CharField(max_length=32, default="-1", null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.refereeNumber})"


class LichessAPIError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
