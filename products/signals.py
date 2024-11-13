# product/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
import requests

@receiver(post_save, sender=Product)
def notify_product_added(sender, instance, created, **kwargs):
    if created:
        # Envoie une notification via Soketi
        requests.post("http://localhost:6001/notify", json={
            'event': 'product.added',
            'data': {'product_name': instance.name, 'product_price': instance.price}
        })
