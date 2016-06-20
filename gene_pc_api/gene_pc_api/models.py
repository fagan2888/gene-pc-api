import uuid

from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return '<API: User: %s' % self.email


class Condition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True)
    overview = models.CharField(max_length=1024, blank=True)
    description = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        return '<API: Condition: %s>' % self.name


class Population(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '<API: Population: %s>' % self.name


class RiskScore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True)
    value = models.FloatField(max_length=100, blank=True, default=-1.0)
    description = models.CharField(max_length=1024, blank=True)
    user = models.ForeignKey(User, related_name='risk_scores',
        on_delete=models.PROTECT)
    condition = models.ForeignKey(Condition, related_name='risk_scores',
        on_delete=models.PROTECT)
    population = models.ForeignKey(Population, related_name='risk_scores',
        on_delete=models.PROTECT)
    calculated = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'condition', 'population')

    def __str__(self):
        return '<API: RiskScore: %s %s %s' % (self.user.email, self.condition,
            self.population)


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)
    study_task_identifier = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '<API: Activity: %s' % (self.name)


class ActivityStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='activity_statuses',
        on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, related_name='activity_statuses',
        on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'activity')


class ActivityAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_identifier = models.CharField(max_length=100, blank=True)
    value = models.CharField(max_length=1000, blank=True)
    activity = models.ForeignKey(Activity, related_name='activity_answers',
        on_delete=models.PROTECT, blank=True)
    user = models.ForeignKey(User, related_name='activity_answers',
        on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return '<API: ActivityAnswer: %s %s' % (self.user.email, self.question_identifier)


# Signals

@receiver(post_save, sender=User)
def create_related_models_for_user(sender, instance, created, **kwargs):
    if not created:
        return
    # New Empty Activity Statuses
    for activity in Activity.objects.all():
        status = ActivityStatus(user=instance, activity=activity)
        status.save()
