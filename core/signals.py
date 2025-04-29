# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from core.models import Theater
import requests, os, urllib.parse

API_KEY = getattr(settings, 'GOOGLE_PLACES_KEY', None) or os.getenv('GOOGLE_PLACES_KEY')

def google_geocode(query: str):
    q = urllib.parse.quote(query)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={q}&key={API_KEY}"
    try:
        res = requests.get(url, timeout=5).json()
        if res['status'] == 'OK':
            loc = res['results'][0]['geometry']['location']
            return loc['lat'], loc['lng']
    except Exception as e:
        print('[geo ERR]', e)
    return None, None

@receiver(post_save, sender=Theater)
def auto_geocode_async(sender, instance: Theater, created, **_):
    if instance.lat and instance.lng:
        return

    import threading
    def worker(pk):
        th = Theater.objects.get(pk=pk)
        if th.lat and th.lng:
            return
        lat, lng = google_geocode(th.address or f"{th.name} Japan")
        if lat:
            Theater.objects.filter(pk=pk).update(lat=lat, lng=lng)
    threading.Thread(target=worker, args=(instance.pk,), daemon=True).start()
