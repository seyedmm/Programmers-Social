from django.db import models
from django_jalali.db import models as jmodels
from django.utils import timezone

class Person(models.Model):
    PROGRAMMING_CHOICES = (
        ('C Language', 'C Language'),
        ('C++', 'C++'),
        ('C#', 'C#'),
        ('Objective-C', 'Objective-C'),
        ('Java', 'Java'),
        ('JavaScript', 'JavaScript'),
        ('Python', 'Python'),
        ('PHP', 'PHP'),
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('Perl', 'Perl'),
        ('Swift', 'Swift'),
        ('Kotlin', 'Kotlin'),
        ('Go', 'Go'),
        ('Ruby', 'Ruby'),
        ('Basic', 'Basic'),
        ('Pascal', 'Pascal'),
        ('Lua', 'Lua'),
        ('R Language', 'R Language'),
        ('Rust', 'Rust'),
        ('TypeScript', 'TypeScript'),
    )
    
    YEARS = []

    for year in range(1330, 1395):
        YEARS.append((str(year), str(year)),)

    YEARS = tuple(YEARS)

    # Personal detail
    username = models.CharField(max_length = 50, verbose_name = 'نام کاربری')
    avatar = models.ImageField(upload_to = 'avatars/', blank = True, verbose_name = 'آواتار')
    name = models.CharField(max_length = 50, verbose_name = 'نام')
    public_email = models.CharField(max_length = 100, null = True, blank = True, verbose_name = 'پست الکترونیک')
    mobile = models.CharField(max_length = 11, null = True, blank = True, verbose_name = 'شماره تماس')
    description = models.CharField(max_length = 200, null = True, blank = True, verbose_name = 'توضیحات')
    year_of_born = models.CharField(max_length = 4, choices = YEARS, null = True, blank = True, verbose_name = 'سال تولد')
    gender = models.CharField(max_length = 10, null = True, blank = True, verbose_name = 'جنسیت')

    # Work detail
    work = models.CharField(max_length = 50, null = True, blank = True, verbose_name = 'تخصص')
    programming = models.ManyToManyField('Programming', blank = True, verbose_name = 'زبان‌های برنامه نویسی')
    rezome = models.TextField(null = True, blank = True, default = '', verbose_name = 'رزومه')

    # Statistic detail
    likes = models.ManyToManyField('Post', blank = True, verbose_name = 'لایک‌ها')
    viewed_posts = models.ManyToManyField('Post', related_name = 'views_post', blank = True, verbose_name = 'مطالب مشاهده شده')
    following = models.ManyToManyField('Person', blank = True, verbose_name = 'دنبال شوندگان')
    len_following = models.CharField(max_length = 10, default = 0, verbose_name = 'تعداد دنبال شوندگان')
    followers = models.ManyToManyField('Person', related_name = 'folllowers', blank = True, verbose_name = 'دنبال کنندگان')
    len_followers = models.CharField(max_length = 10, default = 0, verbose_name = 'تعداد دنبال کنندگان')
    
    # Social detail
    github = models.URLField(null = True, blank = True, verbose_name = 'گیت‌هاب')
    gitlab = models.URLField(null = True, blank = True, verbose_name = 'گیت‌لب')
    stackowerflow = models.URLField(null = True, blank = True, verbose_name = 'استک اورفلو')
    linkedin = models.URLField(null = True, blank = True, verbose_name = 'لینکدین')
    dev = models.URLField(null = True, blank = True, verbose_name = 'جامعه دِو')
    website = models.URLField(null = True, blank = True, verbose_name = 'وبسایت')

    class Meta:
        verbose_name = 'فرد'
        verbose_name_plural = 'افراد'

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length = 50, verbose_name = 'عنوان')
    body = models.TextField(verbose_name = 'متن')
    cover = models.CharField(max_length = 1000, null = True, blank = True, verbose_name = 'کاور')
    category = models.CharField(max_length = 50, verbose_name = 'دسته بندی', null = True)
    short_description = models.TextField(max_length = 156, null = True, blank = True, verbose_name = 'توضیح کوتاه')
    author = models.ForeignKey('Person', on_delete = models.SET_NULL, null = True, verbose_name = 'نویسنده')
    publish_time = jmodels.jDateTimeField(default = timezone.now, verbose_name = 'زمان انتشار')

    # Statistic
    comments = models.CharField(max_length = 10, default = '0', verbose_name = 'تعداد نظر')
    likes = models.CharField(max_length = 10, default = '0', verbose_name = 'تعداد لایک')
    views = models.CharField(max_length = 10, default = '0', verbose_name = 'تعداد بازدید')

    class Meta:
        verbose_name = 'مطلب'
        verbose_name_plural = 'مطالب'

    def __str__(self):
        return self.title


class PostComment(models.Model):
    place = models.ForeignKey('Post', on_delete = models.SET_NULL, null = True, verbose_name = 'مکان')
    author = models.ForeignKey('Person', on_delete = models.SET_NULL, null = True, verbose_name = 'نویسنده')
    text = models.CharField(max_length = 1000, verbose_name = 'متن')
    replay = models.CharField(max_length = 1000, null = True, blank = True, verbose_name = 'پاسخ')

    class Meta:
        verbose_name = 'نظر مطلب'
        verbose_name_plural = 'نظرات مطالب'


class Ad(models.Model):
    post = models.ForeignKey('Post', on_delete = models.SET_NULL, null = True, verbose_name = 'مطلب')
    type = models.CharField(max_length = 50, verbose_name = 'نوع')
    available_views = models.CharField(max_length = 10, default = 100, verbose_name = 'بازدید باقی مانده')

    class Meta:
        verbose_name = 'تبلیغ'
        verbose_name_plural = 'تبلیغات'

class Programming(models.Model):
    language = models.CharField(max_length = 50, verbose_name = 'زبان برنامه نویسی')

    class Meta:
        verbose_name = 'زبان برنامه نویسی'
        verbose_name_plural = 'زبان‌های برنامه نویسی'

    def __str__(self):
        return self.language


class Notification(models.Model):
    givver = models.ForeignKey('Person', on_delete = models.SET_NULL, null = True, verbose_name = 'گیرنده')
    message = models.TextField(verbose_name = 'متن پیام')
    notif_type = models.CharField(max_length = 10, null = True, default = None, verbose_name = 'نوع')
    done = models.BooleanField(default = False, verbose_name = 'خوانده شده')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام‌ها'

    
class Cloud(models.Model):
    owner = models.ForeignKey('Person', on_delete = models.SET_NULL, null = True, verbose_name = 'صاحب')
    space = models.CharField(max_length = 100, default = 100, verbose_name = 'فضا')
    used_space = models.CharField(max_length = 100, default = 0, verbose_name = 'فضای استفاده شده')
    used_percent = models.CharField(max_length = 10, default = 0, verbose_name = 'درصد استفاده شده')

    class Meta:
        verbose_name = 'ابر'
        verbose_name_plural = 'ابر‌ها'

    def __str__(self):
        return 'ابر {}'.format(self.owner.name)


class File(models.Model):
    cloud = models.ForeignKey('Cloud', on_delete = models.SET_NULL, null = True, verbose_name = 'ابر')
    file = models.ImageField(upload_to = 'images/', blank = True, verbose_name = 'فایل')