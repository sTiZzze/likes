from django.conf import settings
from django.db import models
from django_fsm import FSMField


def upload_update_image(instance, filename):
    return "updates/{user}/{filename}".format(user=instance.user, filename=filename)


class State(models.TextChoices):
    LIKE = 'Like'
    Report = 'Report'
    SKIP = 'Skip'


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_update_image, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now_add=True, db_index=True)
    state = FSMField(choices=State.choices, protected=False, default=State.LIKE)
