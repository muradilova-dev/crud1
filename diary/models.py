from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField("Страна", max_length=100)
    dish = models.CharField("Блюдо", max_length=200)
    description = models.TextField("Впечатления", blank=True)
    photo = models.ImageField("Фото", upload_to='dishes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dish} — {self.country}"