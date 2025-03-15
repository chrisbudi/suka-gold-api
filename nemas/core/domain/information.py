from django.db import models


class information_educational(models.Model):
    information_educational_id = models.AutoField(primary_key=True)
    information_name = models.CharField(max_length=255)
    information_notes = models.TextField(blank=True, null=True)
    information_url = models.URLField(max_length=200, blank=True, null=True)
    information_background = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.UUIDField(null=True)
    create_user_mail = models.CharField(max_length=255, null=True)

    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.UUIDField(null=True)
    upd_user_mail = models.CharField(max_length=255, null=True)

    def update_image_path(self, fileUrl):
        self.information_background = fileUrl
        self.save()
        return f"information/{self.information_name}/{self.information_url}"

    def __str__(self):
        return self.information_name


class information_faq(models.Model):
    information_faq_id = models.AutoField(primary_key=True)
    information_title = models.CharField(max_length=255)
    information_question = models.TextField(blank=True, null=True)
    information_answer = models.TextField(blank=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.UUIDField(null=True)
    create_user_mail = models.CharField(max_length=255, null=True)

    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.UUIDField(null=True)
    upd_user_mail = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.information_title


class information_customer_service(models.Model):
    information_customer_service_id = models.AutoField(primary_key=True)
    information_phone = models.CharField(max_length=20)
    information_name = models.CharField(max_length=255)

    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.UUIDField(null=True)
    create_user_mail = models.CharField(max_length=255, null=True)

    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.UUIDField(null=True)
    upd_user_mail = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.information_name


class information_rating(models.Model):
    information_rate_id = models.AutoField(primary_key=True)
    information_rate_name = models.CharField(max_length=255)
    rate = models.IntegerField()
    message = models.TextField(blank=True, null=True)
    publish = models.BooleanField(default=False)

    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.UUIDField(null=True)
    create_user_mail = models.CharField(max_length=255, null=True)

    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.UUIDField(null=True)
    upd_user_mail = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.information_rate_name


class information_article(models.Model):
    information_article_id = models.AutoField(primary_key=True)
    information_article_name = models.CharField(max_length=255)
    information_article_body = models.TextField(blank=True, null=True)
    article_date = models.DateTimeField(blank=True, null=True)
    article_publish_date = models.DateTimeField(blank=True, null=True)
    article_updated_date = models.DateTimeField(blank=True, null=True)
    article_author = models.CharField(max_length=255, blank=True, null=True)
    article_source = models.URLField(max_length=255, blank=True, null=True)
    article_link = models.URLField(max_length=255, blank=True, null=True)
    article_background = models.URLField(max_length=255, blank=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.UUIDField(null=True)
    create_user_mail = models.CharField(max_length=255, null=True)

    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.UUIDField(null=True)
    upd_user_mail = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.information_article_name


class information_promo(models.Model):
    promo_id = models.AutoField(primary_key=True)
    promo_code = models.CharField(max_length=255)  # kode untuk dapat promo
    leveling_user = models.CharField(max_length=50)  # all level, silver, gold, platinum
    promo_name = models.CharField(max_length=255)
    promo_url = models.CharField(max_length=255)
    promo_start_date = models.DateTimeField()
    promo_end_date = models.DateTimeField()
    promo_tag = models.CharField(max_length=255)  # SHARE
    promo_url_background = models.CharField(max_length=255)
    promo_diskon = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )  # Optional
    promo_cashback = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )  # Optional
    promo_cashback_tipe_user = models.CharField(
        max_length=255, blank=True, null=True
    )  # Optional
    merchant_cashback = models.CharField(
        max_length=255, blank=True, null=True
    )  # Optional
    show_banner = models.BooleanField(default=True)

    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.UUIDField(null=True)
    create_user_mail = models.CharField(max_length=255, null=True)

    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.UUIDField(null=True)
    upd_user_mail = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.promo_name
