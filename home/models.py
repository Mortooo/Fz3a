from django.db import models


class SiteSettings(models.Model):
    """إعدادات الموقع العامة: النصوص الثابتة والروابط"""

    class Meta:
        verbose_name = "إعدادات الموقع"
        verbose_name_plural = "إعدادات الموقع"

    # الهوية
    site_name = models.CharField("اسم الموقع", max_length=255, default="مبادرة فزعة المحتاج الخيرية")
    tagline = models.CharField("الوصف المختصر", max_length=255, default="مبادرة خيرية تطوعية")
    logo = models.ImageField("الشعار", upload_to='', blank=True, null=True)
    hashtag = models.CharField("الهاشتاق", max_length=100, default="#يلا_نسندهم")
    hero_headline = models.CharField("عنوان الواجهة الرئيسية", max_length=255, default="معاً نصنع أثراً… ومعاً نمد يد العون")
    hero_intro = models.TextField("مقدمة الواجهة الرئيسية", default="", blank=True)

    # القصة / الرسالة / الرؤية
    story_badge = models.CharField("شارة القصة", max_length=100, default="قصتنا")
    story_headline = models.CharField("عنوان القصة", max_length=255, default="سبع سنوات من العطاء والتكاتف المجتمعي")
    story_paragraphs = models.TextField("فقرات القصة (افصل بينها بسطر فارغ)", default="", blank=True,
                                        help_text="افصل بين كل فقرة وسطر فارغ")
    mission_title = models.CharField("عنوان الرسالة", max_length=100, default="رسالتنا")
    mission_text = models.TextField("نص الرسالة", default="", blank=True)
    vision_title = models.CharField("عنوان الرؤية", max_length=100, default="رؤيتنا")
    vision_text = models.TextField("نص الرؤية", default="", blank=True)

    # الروابط الاجتماعية
    whatsapp_link = models.URLField("رابط الواتساب", blank=True, default="")
    facebook_link = models.URLField("رابط الفيسبوك", blank=True, default="")

    # اسم المستفيد في شاشة التبرع
    donation_name = models.CharField("باسم (للتبرع)", max_length=255, default="", blank=True)

    def __str__(self):
        return self.site_name

    def get_story_paragraphs(self):
        if not self.story_paragraphs:
            return []
        return [p.strip() for p in self.story_paragraphs.split("\n") if p.strip()]

    def save(self, *args, **kwargs):
        # التأكد من وجود سجل واحد فقط
        self.pk = 1
        super().save(*args, **kwargs)


class CoreValue(models.Model):
    """قيم المبادرة"""

    class Meta:
        verbose_name = "قيمة"
        verbose_name_plural = "قيم المبادرة"
        ordering = ['order']

    title = models.CharField("العنوان", max_length=100)
    description = models.TextField("الوصف")
    icon = models.CharField("أيقونة FontAwesome", max_length=50, default="fa-solid fa-heart-pulse",
                            help_text="مثال: fa-solid fa-heart-pulse")
    order = models.PositiveIntegerField("الترتيب", default=0)

    def __str__(self):
        return self.title


class FieldOfWork(models.Model):
    """مجالات العمل"""

    class Meta:
        verbose_name = "مجال عمل"
        verbose_name_plural = "مجالات العمل"
        ordering = ['order']

    title = models.CharField("العنوان", max_length=100)
    description = models.TextField("الوصف")
    footer_note = models.CharField("سطر سفلي", max_length=200, blank=True, default="")
    icon = models.CharField("أيقونة FontAwesome", max_length=50, default="fa-solid fa-hand-holding-heart")
    color = models.CharField("اللون (روز/كهرماني/أزرق)", max_length=30, default="rose",
                             help_text="rose / amber / blue")
    order = models.PositiveIntegerField("الترتيب", default=0)

    def __str__(self):
        return self.title

    @property
    def color_classes(self):
        return {
            'rose': {'border': 'hover:border-rose-300', 'icon_bg': 'bg-rose-50', 'icon_color': 'text-rose-600', 'footer': 'text-rose-600'},
            'amber': {'border': 'hover:border-amber-300', 'icon_bg': 'bg-amber-50', 'icon_color': 'text-amber-600', 'footer': 'text-amber-600'},
            'blue': {'border': 'hover:border-blue-300', 'icon_bg': 'bg-blue-50', 'icon_color': 'text-blue-600', 'footer': 'text-blue-600'},
        }.get(self.color, {'border': 'hover:border-emerald-300', 'icon_bg': 'bg-emerald-50', 'icon_color': 'text-emerald-600', 'footer': 'text-emerald-600'})


class Project(models.Model):
    """المشاريع الموسمية"""

    class Meta:
        verbose_name = "مشروع"
        verbose_name_plural = "المشاريع"
        ordering = ['order']

    title = models.CharField("العنوان", max_length=100)
    description = models.TextField("الوصف")
    badge = models.CharField("الشارة", max_length=100, default="مشروع موسمي")
    icon = models.CharField("أيقونة FontAwesome", max_length=50, default="fa-solid fa-moon")
    gradient = models.CharField("درجات الألوان", max_length=100, default="from-emerald-950 via-slate-900 to-slate-950")
    order = models.PositiveIntegerField("الترتيب", default=0)

    def __str__(self):
        return self.title


class GalleryItem(models.Model):
    """عناصر معرض الأثر: صور وفيديوهات"""

    class MediaType(models.TextChoices):
        PHOTO = 'photo', 'صورة'
        VIDEO = 'video', 'فيديو'

    class Meta:
        verbose_name = "عنصر معرض"
        verbose_name_plural = "معرض الأثر"
        ordering = ['order']

    media_type = models.CharField("النوع", max_length=10, choices=MediaType.choices, default=MediaType.PHOTO)
    title = models.CharField("العنوان", max_length=255)
    subtitle = models.CharField("العنوان الفرعي", max_length=255, blank=True, default="")
    file = models.FileField("الملف", upload_to='Gallary/', blank=True, null=True)
    # دعم المسار المباشر للنظام القديم
    direct_url = models.CharField("مسار مباشر (اختياري)", max_length=500, blank=True, default="",
                                  help_text="استخدمه للتوافق مع الملفات الموجودة في مجلد Gallary، مثال: Gallary/اسم الملف.jpg")
    order = models.PositiveIntegerField("الترتيب", default=0)
    active = models.BooleanField("ظاهر", default=True)

    def __str__(self):
        return self.title

    @property
    def media_url(self):
        if self.file:
            return self.file.url
        if self.direct_url:
            return "/" + self.direct_url.lstrip("/")
        return ""


class VolunteerApplication(models.Model):
    """طلبات التسجيل للتطوع"""

    class Status(models.TextChoices):
        NEW = 'new', 'جديد'
        CONTACTED = 'contacted', 'تم التواصل'
        ACCEPTED = 'accepted', 'مقبول'
        REJECTED = 'rejected', 'مرفوض'

    class Meta:
        verbose_name = "طلب تطوع"
        verbose_name_plural = "طلبات التطوع"
        ordering = ['-created_at']

    full_name = models.CharField("الاسم الكامل", max_length=200)
    phone = models.CharField("رقم الجوال / واتساب", max_length=50)
    email = models.EmailField("البريد الإلكتروني", blank=True, default="")
    city = models.CharField("المدينة", max_length=100, blank=True, default="")
    interest = models.TextField("مجالات الاهتمام أو الخبرات", blank=True, default="",
                                help_text="مثال: العمل الميداني، التواصل، التصوير، الطب، التقنية...")
    availability = models.CharField("أوقات التوفر", max_length=200, blank=True, default="")
    message = models.TextField("رسالة إضافية", blank=True, default="")
    status = models.CharField("الحالة", max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField("تاريخ التقديم", auto_now_add=True)

    def __str__(self):
        return self.full_name or "طلب تطوع"


class DonationMethod(models.Model):
    """طرق المساهمة: الحسابات المصرفية والرصيد"""

    class Meta:
        verbose_name = "طريقة مساهمة"
        verbose_name_plural = "طرق المساهمة"
        ordering = ['order']

    class Category(models.TextChoices):
        BANK = 'bank', 'حسابات مصرفية'
        MOBILE = 'mobile', 'المساهمة عبر الرصيد'

    name = models.CharField("الاسم/الوصف", max_length=100)  # مثال: تطبيق بنكك (Bankak)
    number = models.CharField("الرقم", max_length=100)
    category = models.CharField("الفئة", max_length=10, choices=Category.choices, default=Category.BANK)
    order = models.PositiveIntegerField("الترتيب", default=0)

    def __str__(self):
        return self.name
