from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from datetime import date




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
        from_email='Zayrac7@yandex.ru',
        to=kwargs['user_emails']
    )
    msg.attach_alternative(html, 'text/html')
    msg.send()


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


def notify_subscribers_weekly():
    template = 'subcat/weekly_digest.html'
    week = 7
    week_sec = week*24*60*60
    print(week)
    posts = Post.objects.all()
    posts_list = []
    cat_list = set()
    sub_list = set()

    for post in posts:
        interval_week = date.today() - post.date.date()
        if interval_week.total_seconds() < week_sec:
            posts_list.append(post)
            for category in post.category.all():
                if get_subscribers(category):
                    sub_list.update(get_subscribers(category))
                    cat_list.add(category)
    print(f'cat_list - {cat_list}')
    print(f'sub_list - {sub_list}')
    for user_email in sub_list:
        post_object = []
        category_set = set()

        for post in posts_list:
            for category in post.category.all():
                if get_subscribers(category):
                    for user in category.subscribers.all():
                        if user.email == user_email:
                            post_object.append(post)
                            category_set.add(category)
                            print(f"Done {category} + {user.id}")

        category_object = list(category_set)

        send_emails(
            post_object,
            category_object=category_object,
            email_subject="Новости за неделю по вашей подписке",
            template=template,
            user_emails=[user_email, ])