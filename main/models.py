from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings


class Person(models.Model):
    YEARS = []
    for year in range(1330, 1395):
        YEARS.append((str(year), str(year)),)

    YEARS = tuple(YEARS)

    # Personal detail
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='کاربر'
    )
    username = models.CharField(
        max_length=50,
        verbose_name='نام کاربری'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        verbose_name='آواتار'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='نام'
    )
    public_email = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='پست الکترونیک'
    )
    mobile = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        verbose_name='شماره تماس'
    )
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='توضیحات'
    )
    year_of_born = models.CharField(
        max_length=4,
        choices=YEARS,
        null=True,
        blank=True,
        verbose_name='سال تولد'
    )
    gender = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name='جنسیت'
    )
    join_time = jmodels.jDateTimeField(
        default=timezone.now,
        verbose_name='زمان عضویت'
    )

    # Work detail
    work = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='تخصص'
    )
    skills = models.ManyToManyField(
        'Skill',
        blank=True,
        verbose_name='مهارت‌ها'
    )
    rezome = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='رزومه'
    )

    # Statistic detail
    liked_posts = models.ManyToManyField(
        'Post',
        blank=True,
        verbose_name='لایک‌ها'
    )
    viewed_posts = models.ManyToManyField(
        'Post',
        related_name='views_post',
        blank=True,
        verbose_name='مطالب مشاهده شده'
    )
    following = models.ManyToManyField(
        'Person',
        blank=True,
        verbose_name='دنبال شوندگان'
    )
    len_following = models.CharField(
        max_length=10,
        default=0,
        verbose_name='تعداد دنبال شوندگان'
    )
    followers = models.ManyToManyField(
        'Person',
        related_name='folllowers',
        blank=True,
        verbose_name='دنبال کنندگان'
    )
    len_followers = models.CharField(
        max_length=10,
        default=0,
        verbose_name='تعداد دنبال کنندگان'
    )

    # Social detail
    github = models.URLField(
        null=True,
        blank=True,
        verbose_name='گیت هاب'
    )
    gitlab = models.URLField(
        null=True,
        blank=True,
        verbose_name='گیت لب'
    )
    stackowerflow = models.URLField(
        null=True,
        blank=True,
        verbose_name='استک اورفلو'
    )
    linkedin = models.URLField(
        null=True,
        blank=True,
        verbose_name='لینکدین'
    )
    dev = models.URLField(
        null=True,
        blank=True,
        verbose_name='جامعه دِو'
    )
    website = models.URLField(
        null=True,
        blank=True,
        verbose_name='وبسایت'
    )

    class Meta:
        verbose_name = 'فرد'
        verbose_name_plural = 'افراد'

    def __str__(self):
        return self.username


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Person.objects.create(
                user=instance,
                username=instance.username
            )

        except:
            pass


post_save.connect(
    post_save_user_model_receiver,
    sender=settings.AUTH_USER_MODEL
)


class Post(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='عنوان'
    )
    body = models.TextField(
        verbose_name='متن'
    )
    cover = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name='کاور'
    )
    category = models.CharField(
        max_length=50,
        null=True,
        verbose_name='دسته بندی'
    )
    short_description = models.TextField(
        max_length=156,
        null=True,
        blank=True,
        verbose_name='توضیح کوتاه'
    )
    author = models.ForeignKey(
        'Person',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='نویسنده'
    )
    publish_time = jmodels.jDateTimeField(
        default=timezone.now,
        verbose_name='زمان انتشار'
    )

    # Statistic
    comments = models.CharField(
        max_length=10,
        default='0',
        verbose_name='تعداد نظر'
    )
    likes = models.CharField(
        max_length=10,
        default='0',
        verbose_name='تعداد لایک'
    )
    views = models.CharField(
        max_length=10,
        default='0',
        verbose_name='تعداد بازدید'
    )

    class Meta:
        verbose_name = 'مطلب'
        verbose_name_plural = 'مطالب'

    def __str__(self):
        return self.title


class Comment(models.Model):
    place = models.ForeignKey(
        'Post',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='مکان'
    )
    author = models.ForeignKey(
        'Person',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='نویسنده'
    )
    text = models.CharField(
        max_length=1000,
        verbose_name='متن'
    )
    replays = models.ManyToManyField(
        'Comment',
        blank=True,
        verbose_name='پاسخ‌ها'
    )
    submit_time = jmodels.jDateTimeField(
        default=timezone.now,
        verbose_name='زمان ثبت'
    )

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class Ad(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='مطلب'
    )
    type = models.CharField(
        max_length=50,
        verbose_name='نوع'
    )
    available_views = models.CharField(
        max_length=10,
        default=100,
        verbose_name='بازدید باقی مانده'
    )

    class Meta:
        verbose_name = 'تبلیغ'
        verbose_name_plural = 'تبلیغات'


class Skill(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='مهارت'
    )

    class Meta:
        verbose_name = 'مهارت'
        verbose_name_plural = 'مهارت‌ها'

    def __str__(self):
        return self.name


class Notification(models.Model):
    givver = models.ForeignKey(
        'Person',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='گیرنده'
    )
    message = models.TextField(
        verbose_name='متن پیام'
    )
    notif_type = models.CharField(
        max_length=10,
        default=None,
        null=True,
        verbose_name='نوع'
    )
    done = models.BooleanField(
        default=False,
        verbose_name='خوانده شده'
    )

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام‌ها'


class Cloud(models.Model):
    owner = models.ForeignKey(
        'Person',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='صاحب'
    )
    space = models.CharField(
        max_length=100,
        default=100,
        verbose_name='فضا'
    )
    used_space = models.CharField(
        max_length=100,
        default=0,
        verbose_name='فضای استفاده شده'
    )
    used_percent = models.CharField(
        max_length=10,
        default=0,
        verbose_name='درصد استفاده شده'
    )

    class Meta:
        verbose_name = 'ابر'
        verbose_name_plural = 'ابر‌ها'

    def __str__(self):
        return 'ابر {}'.format(self.owner.name)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Cloud.objects.create(owner=instance)

        except:
            pass


post_save.connect(
    post_save_user_model_receiver,
    sender=settings.AUTH_USER_MODEL
)


class File(models.Model):
    cloud = models.ForeignKey(
        'Cloud',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='ابر'
    )
    file = models.ImageField(
        upload_to='images/',
        blank=True,
        verbose_name='فایل'
    )
