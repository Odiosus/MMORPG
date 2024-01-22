from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from MMORPG.MMORPG import settings
from MMORPG.msg_board.models import NewsForSubscribers, SubscriberNews


def send_email_notify(reply, title, template, subscribers_email):
    html_mail = render_to_string(
        'news_for_subscribers.html',
        {
            'text': reply,
        }
    )

    message = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email
    )

    message.attach_alternative(html_mail, 'text/html')
    message.send()


@receiver(post_save, sender=NewsForSubscribers)
def send_news(sender, instance, **kwargs):
    if not instance.draft:
        subscribers = set(SubscriberNews.objects.all())
        subscribers_emails = []
        for sub_users in subscribers:
            subscribers_emails.append(sub_users.user.email)
        print(subscribers_emails)
        send_email_notify(instance.content, f'{instance.title}',
                          'msg_board/news_for_subscribers.html', subscribers_emails)
