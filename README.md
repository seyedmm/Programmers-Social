<div dir="rtl">

# شبکه اجتماعی برنامه نویسان
[![CodeFactor](https://www.codefactor.io/repository/github/mskf1383/programmers-social/badge)](https://www.codefactor.io/repository/github/mskf1383/programmers-social)
![CodeQL](https://github.com/mskf1383/Programmers-Social/workflows/CodeQL/badge.svg)
![GitHub](https://img.shields.io/github/license/mskf1383/Programmers-Social)


این یک  شبکه اجتماعی متن باز و رایگان است که با پایتون و جنگو نوشته شده است. هدف این شبکه اجتماعی برنامه نویسان هستند. در تاریخ ۱۴۰۰/۰۱/۰۱ منتظر افتتاح این شبکه اجتماعی باشید.
اگر در برنامه نویسی پایتون و جنگو مهارت دارید در صورت علاقه در توسعه این شبکه اجتماعی کمک کنید.

### نام و لوگو از پیش انتخاب شده و در ~۱۴۰۰/۰۱/۰۱~ `۱۴۰۰/۰۶/۲۱` رونمایی می‌شود

- توجه: افتتاح پروژه به ۲۱ شهریور ۱۴۰۰ مصادف با روز برنامه نویس موکول شد


نسخه دمو: http://mskf1383.pythonanywhere.com/

**توجه:** ممکن است نسخه دمو به روز نباشد.

**توجه:** بعد از هر به روز رسانی دیتابیس نسخه دمو با دیتابیس داخل ریپوزیتوری جایگزین می‌شود.


## ویژگی‌های این شبکه اجتماعی
- 👨‍💻 فقط برای برنامه نویسان
- 📜 مطلب محور
- 😀 پروفایل کامل
- 💲 امکان دونیت (در آینده)
- 💬 امکان چت بین کاربران (در آینده)


## مشارکت در پروژه
- اگر مشکل یا باگی پیدا کردید در بخش [Issues](https://github.com/mskf1383/Programmers-Social/issues) مطرح کنید
- اگر سوال، پیشنهاد یا انتقادی داشتید در بخش [Discussions](https://github.com/mskf1383/Programmers-Social/discussions) مطرح کنید

اعمال تغییر در کدها:
- سعی کنید کدها در چارچوب [pep8](http://pep8.org/) بنویسید
- از ارسال کامیت‌های بزرگ خودداری کنید
- قبل از انجام تغییرات اساسی با ایمیل mskf1383@protonmail.com هماهنگ کنید


## دستورالعمل استفاده
پس از دانلود رپوزیتوری آن را استخراج کنید و در کامند لاین (Terminal, CMD,...) با دستور cd به داخل پوشه آن بروید سپس دستورات زیر را به ترتیب وارد کنید.

نصب محیط ایزوله:
</div>

```
pip3 install virtualenv
```
<div dir="rtl">

ایجاد محیط ایزوله:
</div>

```
vitualenv -p python3 venv
```
<div dir="rtl">

وارد شدن به محیط ایزوله:
</div>

```
source venv/bin/activate
```
<div dir="rtl">

در ویندوز: `venv\Scripts\activate`

نصب نیازمندی‌ها:
</div>

```
pip install -r requirements.txt
```
<div dir="rtl">

پیکربندی پروژه:
</div>

```
python manage.py migrate
```
<div dir="rtl">

اجرای پروژه:
</div>

```
python manage.py runserver
```
<div dir="rtl">

اکنون با وارد کردن آدرس `localhost:8000` در مرورگر وارد سایت می‌شوید.


## مجوز
این پروژه تحت مجوز [MPL-2](https://github.com/mskf1383/Programmers-Social/blob/main/LICENSE) منشتر شده است.
</div>
