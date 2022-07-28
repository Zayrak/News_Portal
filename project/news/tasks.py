from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string


def get_subscribers(category):
    user_emails = []
    for user in category.subscribers.all():
        user_emails.append(user.email)
    return user_emails


def send_emails(post_object, *args, **kwargs):
    html = render_to_string(
        kwargs['template'],
        {'category_object': kwargs['category_object'], 'post_object': post_object},
    )
    print(f'category: {kwargs["category_object"]}')
    msg = EmailMultiAlternatives(
        subject=kwargs['email_subject'],
        from_email='*******@yandex.ru',
        to=kwargs['user_emails']
    )
    msg.attach_alternative(html, 'text/html')


def new_post_subscription(instance):
    template = 'subcat/newpost.html'
    latest_post = instance
    for category in latest_post.category.all():
        email_subject = f'Новая новость в категории: "{category}"'
        user_emails = get_subscribers(category)
        send_emails(
            latest_post,
            category_object=category,
            email_subject=email_subject,
            template=template,
            user_emails=user_emails)
