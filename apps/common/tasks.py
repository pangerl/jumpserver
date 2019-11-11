from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from .utils import get_logger
from .models import Setting
import requests


logger = get_logger(__file__)


@shared_task
def send_mail_async(*args, **kwargs):
    """ Using celery to send email async

    You can use it as django send_mail function

    Example:
    send_mail_sync.delay(subject, message, from_mail, recipient_list, fail_silently=False, html_message=None)

    Also you can ignore the from_mail, unlike django send_mail, from_email is not a require args:

    Example:
    send_mail_sync.delay(subject, message, recipient_list, fail_silently=False, html_message=None)
    """
    if len(args) == 3:
        args = list(args)
        args[0] = settings.EMAIL_SUBJECT_PREFIX + args[0]
        args.insert(2, settings.EMAIL_HOST_USER)
        args = tuple(args)
    try:
        data = {
            "to": (None, args[3]),
            "subject": (None, args[0]),
            "text": (None, args[1])
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        logger.error(data)
        url = 'http://10.60.136.199:8090/sendmail'
        #send_mail(*args, **kwargs)
        test = requests.post(url, data=data, headers=headers)
        logger.error(test)
    except Exception as e:
        logger.error("Sending mail error: {}".format(e))
