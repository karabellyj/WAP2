import os
from django.db import models
from hashlib import md5
from django.contrib.auth import get_user_model
from django.urls import reverse


class File(models.Model):
    url_hash = models.URLField(unique=True)
    file = models.FileField(upload_to='uploads/')
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    visits = models.PositiveIntegerField(default=0)

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='files'
    )

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def clicked(self):
        self.visits += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.url_hash = md5(self.file.read()).hexdigest()[:10]

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("file-detail", kwargs={"url": self.url_hash})
