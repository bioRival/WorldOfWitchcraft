from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import PostReply
from django.contrib.auth.models import User


@receiver(post_save, sender=PostReply)
def send_email_to_post_owner(sender, instance, created, **kwargs):
    if created:
        user = instance.post.author.user
        send_mail(
            subject="Ваше объявление получило отклик! " + instance.post.title,
            message = f"Здравствуй, {user.username}. На вашем объявлении появился " \
                      f"новый отклик от {instance.user.username.capitalize()}! " \
                      f"\n{instance.content} \n" \
                      f"Проверь страницу с объявлением: http://127.0.0.1:8000/post/{instance.post.pk}",
            from_email='biorival@yandex.ru',
            recipient_list=[user.email],
            fail_silently=False,
        )