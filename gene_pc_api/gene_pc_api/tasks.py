from celery import shared_task


@shared_task
def send_registration_email_to_user(user):
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )
