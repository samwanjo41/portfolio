from django.db import models
from django.conf import settings

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField()
    main_language = models.CharField(max_length=100)
    premium = models.BooleanField(default=True)
    url_link = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=250)
    stripe_subscription_id = models.CharField(max_length=250)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username