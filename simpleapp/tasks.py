from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import Post
from django.contrib.auth.models import User
from django.core.mail import mail_managers


@shared_task
def post_created(instance, sender, **kwargs):
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


@shared_task
def weekly_send_emails():
    posts = Post.objects.order_by('-added_at')[:3]
    subject = ('3 самых свежих поста')
    text_content = '\n'.join(['{} - {}'.format(p.title, p.added_at) for p in posts])
    mail_managers("Самые свежие посты", text_content)
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.MANAGERS,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(subject, text_content, None, [mail_managers])
    msg.attach_alternative(html_content, "text/html")
    msg.send()