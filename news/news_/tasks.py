from celery import shared_task
import time
from .models import Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from news_.models import Category, News
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string




@shared_task
def notify_subs(**kwargs):
  
       
       subscribers = Category.objects.get(id=kwargs["news_type"]).subscribers.all()
       for subscriber in subscribers:
          
           html_content = render_to_string(
            'mail_template.html',
            {
                "news_title": kwargs["news_title"],
                "news_id":kwargs["news_id"],
                "receiver_name": subscriber.username,
                "short_content":kwargs["news_content"][:50] + "..."
            }
        )
           body_text = f"Новость для вас, {subscriber.username}:\n\n{kwargs["news_content"]}"

           msg = EmailMultiAlternatives(
            subject=kwargs["news_title"],
            body=body_text,
            from_email='newACC-03@yandex.ru',
            to=[subscriber.email]
          )
           msg.attach_alternative(html_content, "text/html")
           msg.send()
       

@shared_task
def weekly_notification():

    
    one_week_ago = timezone.now() - timedelta(weeks=1)
    categories = Category.objects.all()

    for category in categories:
        recent_news = News.objects.filter(type=category, created_at__gte=one_week_ago)

        if recent_news.exists():
          
            text_content = "Свежие новости в категории {} за последнюю неделю:\n\n{}".format(
                category.type,
                "\n".join([f"- {news_item.title}" for news_item in recent_news])
            )

          
            html_content = render_to_string('weekly_email_notification.html', {
                'category': category.type,
                'news_list': recent_news,
            })

            recipient_list = category.subscribers.values_list('email', flat=True)

            if recipient_list:
                subject = f"Новостная рассылка по категории {category.type}"
                from_email = "NewACC-03@yandex.ru"  

                msg = EmailMultiAlternatives(subject, text_content, from_email, list(recipient_list))
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=False)
 



