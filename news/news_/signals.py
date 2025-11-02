from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import time, timedelta
from .models import Category, News
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string




@receiver( post_save, sender = News)
def send_notification_mail(sender, instance, created, **kwargs):
     subs_list = Category.objects.get(type = instance.type.type).subscribers.all()
     print("Working signal at post_save_news!!!")
     for subs in subs_list:
      html_content = render_to_string(
            'mail_template.html',
            {
                "news": instance,
                "receiver_name": subs.username,
                "short_content":instance.content[:50] + "..."
            } 
            )
      msg = EmailMultiAlternatives(
            subject="Новый пост на сайте!",
            body=instance.content,
            from_email='newACC-03@yandex.ru',
            to=[subs.email]
          )
     
      msg.attach_alternative(html_content, "text/html")
      msg.send()
    
