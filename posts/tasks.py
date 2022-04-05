import logging

from celery import shared_task

from posts.models import Post

logger = logging.getLogger(__name__)


@shared_task
def like_post(post_id, user):
    post = Post.objects.get(id=post_id)
    post.like.add(user)
    post.save()
    return True