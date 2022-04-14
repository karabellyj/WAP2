from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import File


@receiver(pre_delete, sender=File)
def my_handler(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(False)