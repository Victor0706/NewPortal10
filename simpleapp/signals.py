from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def new_created(instance, sender, **kwargs):
    if not kwargs['action'] == 'post_add':
        return

    emails = User.objects.filter(
        subscriptions__category__in=instance.postCategory.all()
    ).values_list('email', flat=True)

    subject = f'Свежий пост в категории {instance.postCategory}'

    text_content = (
        f'Пост: {instance.title}\n'
        f'Категория: {instance.postCategory}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Пост: {instance.title}<br>'
        f'Категория: {instance.postCategory}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None,[email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()









