from django.db import models
import requests
from .other_models import LichessAPIError


class Player(models.Model):
    #############################
    # NOTE: General information #
    #############################

    # Player id
    id = models.BigAutoField(primary_key=True)

    # Players name. Can be null or blank
    name = models.CharField(max_length=256, null=True, blank=True)

    # Player's email address. Can be null or blank
    email = models.EmailField(null=True, blank=True)

    # Player's country code (according to ISO 3166-1 standard).
    # Can be null or blank
    country = models.CharField(max_length=2, null=True, blank=True)

    # Date the player was created in the system.
    #  Automatically assigned when the player is created
    creation_date = models.DateTimeField(auto_now_add=True)

    # Date the player's data was last updated.
    # Automatically updated whenever the player is modified
    update_date = models.DateTimeField(auto_now=True)

    #################
    # NOTE: lichess #
    #################

    # Player's username on the Lichess platform.
    # Must be unique and can be null or empty
    lichess_username = models.CharField(
        max_length=150, unique=True, null=True, blank=True
    )

    # Player Lichess rating in Bullet mode. Can be null
    lichess_rating_bullet = models.IntegerField(default=0, null=True)

    # Player Lichess rating in Blitz mode. Can be null
    lichess_rating_blitz = models.IntegerField(default=0, null=True)

    # Player Lichess rating in Rapid mode. Can be null
    lichess_rating_rapid = models.IntegerField(default=0, null=True)

    # Player Lichess rating in Classical mode. Can be null
    lichess_rating_classical = models.IntegerField(default=0, null=True)

    ##############
    # NOTE: fide #
    ##############

    # Unique FIDE identifier of the player. Can be null
    fide_id = models.IntegerField(default=None, unique=True, null=True)

    # Official FIDE rating in Blitz mode. May be null.
    fide_rating_blitz = models.IntegerField(default=0, null=True)

    # Official FIDE rating in Rapid mode. May be null.
    fide_rating_rapid = models.IntegerField(default=0, null=True)

    # Official FIDE rating in Classical mode. May be null.
    fide_rating_classical = models.IntegerField(default=0, null=True)

    ##############
    # NOTE: META #
    ##############
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "email"], name="unique_name_email")
        ]

    def __str__(self):
        return self.lichess_username if self.lichess_username else self.name

    def save(self, *args, **kwargs):
        # Search the user on lichess
        self.get_lichess_user_ratings()

        # Search the player on the database
        existing_player = (
            Player.objects.filter(
                (models.Q(id=self.id) & ~models.Q(id=None))
                | (
                        models.Q(lichess_username=self.lichess_username)
                        & ~models.Q(lichess_username=None)
                )
                | (models.Q(fide_id=self.fide_id) & ~models.Q(fide_id=None))
                | (
                        models.Q(name=self.name, email=self.email)
                        & ~models.Q(name=None)
                        & ~models.Q(email=None)
                )
            )
            .exclude(pk=self.pk)
            .first()
        )

        # If it exists, update the info
        if existing_player:
            for field in self._meta.fields:
                if field.name not in [
                    "id",
                    "creation_date",
                    "lichess_username",
                    "fide_id",
                ]:
                    new_value = getattr(self, field.name)
                    if new_value is not None:
                        setattr(existing_player, field.name, new_value)
            self.id = existing_player.id
            return existing_player.save()
        else:
            # Otherwise, save the current instance as a new player
            return super().save(*args, **kwargs)

    def check_lichess_user_exists(self) -> bool:
        # Check if the field has a value
        if self.lichess_username is None:
            return False

        # Make the request
        response = requests.get(
            f"https://lichess.org/api/user/{self.lichess_username}")

        return response.status_code == 200

    def get_lichess_user_ratings(self) -> None:
        if self.lichess_username is None:
            return

        response = requests.get(
            f"https://lichess.org/api/user/{self.lichess_username}")
        if response.status_code != 200:
            raise LichessAPIError(
                f"Error fetching user "
                f"'{self.lichess_username}'"
                f" data: {response.status_code}"
            )
        data = response.json()
        if data.get("perfs") is None:
            return
        self.lichess_rating_bullet = data["perfs"]["bullet"]["rating"]
        self.lichess_rating_blitz = data["perfs"]["blitz"]["rating"]
        self.lichess_rating_rapid = data["perfs"]["rapid"]["rating"]
        self.lichess_rating_classical = data["perfs"]["classical"]["rating"]
