from django.conf import settings
from django.db import models


def upload_update_image(instance, filename):
    return "updates/{user}/{filename}".format(user=instance.user, filename=filename)


class RandomManager(models.Manager):
    def get_query_set(self):
        return super(RandomManager, self).get_query_set().order_by('?')


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userName')
    image = models.ImageField(upload_to=upload_update_image, blank=True, null=True)
    like = models.IntegerField(default=0)
    report = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = models.Manager()
    randoms = RandomManager()


class View(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='userName')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    view = models.BooleanField(default=False)
