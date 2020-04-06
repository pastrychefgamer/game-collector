from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

class Console(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return f"A {self.color} {self.name}"


class Game(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    rating = models.IntegerField()
    consoles = models.ManyToManyField(Console)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'game_id': self.id})

    def played_for_today(self):
        return self.outcome_set.filter(date=date.today()).count() >= len(HOURS)


HOURS = (
    ('1', '0-4'),
    ('2', '4-6'),
    ('3', '6+'),
)


class Outcome(models.Model):
    date = models.DateField()
    playTime = models.CharField(
        max_length=1,
        choices=HOURS,
        default=HOURS[0][0]
    )

    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_playTime_display()} on {self.date}"

    class Meta:
        ordering = ['-date']
