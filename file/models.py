from django.db import models
from hashlib import md5


class File(models.Model):
    url_hash = models.URLField(unique=True)
    file = models.BinaryField()
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    visits = models.PositiveIntegerField(default=0)

    def clicked(self):
        visits += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.url_hash = md5(self.file.encode()).hexdigest()[:10]
        
        return super().save(*args, **kwargs)
