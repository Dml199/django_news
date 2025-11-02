import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news_.models import Category, News
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


 
logger = logging.getLogger(__name__)

def my_job():
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
 

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
      
        scheduler.add_job(
            my_job,
           trigger=CronTrigger(
                day_of_week="mon", hour="05", minute="00"),  
            id="my_job",  
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="05", minute="00"
            ), 
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")