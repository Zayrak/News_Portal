from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.username}'

    def update_rating(self):
        postR = self.post_set.aggregate(postRating=Sum('rating', default=0))
        pR = 0
        pR += postR.get('postRating')
        comR = self.username.comment_set.aggregate(commentRating=Sum('rating', default=0))
        cR = 0
        cR += comR.get('commentRating')
        cpR = 0
        for pst in self.post_set.all():
            compostR = pst.comment_set.aggregate(commentpostRating=Sum('rating', default=0))
            cpR += compostR.get('commentpostRating')
        self.rating = pR * 3 + cR + cpR
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CatSub', blank=True)

    def __str__(self):
        return f'{self.name}'

    def get_category(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CAT_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    type = models.CharField(max_length=2, choices=CAT_CHOICES, default=ARTICLE)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    text = models.TextField(default='')
    title = models.CharField(max_length=255)
    rating = models.SmallIntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]}...'

    def email_preview(self):
        return f'{self.text[0:50]}...'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def get_cat(self):
        return self.type

    def __str__(self):
        return f'{self.date.date()} :: {self.author} :: {self.title} {self.type}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    # из эталона
    def __str__(self):
        return f'{self.categoryThrough} -> {self.postThrough}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        try:
            return self.post.author.user
        except:
            return self.user.username


class CatSub(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def get_user(self):
        return self.subscriber

    def get_category(self):
        return self.category.name

    def get_cat(self):
        return self.category

    def __str__(self):
        return f'{self.subscriber} - {self.category.name}'
