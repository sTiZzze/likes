from django.conf import settings
from django.db import models


def upload_update_image(instance, filename):
    return "updates/{user}/{filename}".format(user=instance.user, filename=filename)


class RandomManager(models.Manager):
    def get_query_set(self):
        return super(RandomManager, self).get_query_set().order_by('?').distinct('id')


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userName')
    image = models.ImageField(upload_to=upload_update_image, blank=True, null=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    report = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='reports')
    view = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='views')
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = models.Manager()
    randoms = RandomManager()

    @property
    def total_like(self):
        return self.like.count()

    @property
    def total_report(self):
        return self.report.count()

    def block_post(self):
        if self.total_report > 1:
            self.is_blocked = True
