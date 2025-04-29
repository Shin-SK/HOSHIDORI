# core/management/commands/update_nearby_shops.py
from datetime import timedelta
import math, os, requests
import urllib.parse
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from core.models import Theater, Shop, TheaterShop

# ───────── 定数 ─────────
RADIUS_M   = 500          # 検索半径 (m)
MAX_RESULTS = 12          # 取得件数
CACHE_DAYS = 30           # キャッシュ日数

# ───────── ユーティリティ ─────────
def haversine(lat1, lng1, lat2, lng2):
    """2点間の距離を m で返す"""
    R = 6371000
    p = math.pi / 180
    dlat = (lat2 - lat1) * p
    dlng = (lng2 - lng1) * p
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin(dlng / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))

def fetch_places(lat, lng, api_key):
    url = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
           f'?location={lat},{lng}&radius={RADIUS_M}'
           f'&type=restaurant|cafe|bar&key={api_key}')
    res = requests.get(url, timeout=10).json()
    return res.get('results', [])[:MAX_RESULTS]

# ───────── コマンド本体 ─────────
class Command(BaseCommand):
    help = '劇場周辺の飲食店を月1で更新（API: Google Places）'

    def handle(self, *args, **options):
        api_key = (
            getattr(settings, 'GOOGLE_PLACES_KEY', None) or
            os.getenv('GOOGLE_PLACES_KEY')
        )
        if not api_key:
            self.stderr.write('✖ GOOGLE_PLACES_KEY が設定されていません')
            return

        cutoff = timezone.now() - timedelta(days=CACHE_DAYS)
        theaters = Theater.objects.exclude(lat__isnull=True)

        for th in theaters:
            # 協力店／スポンサー以外が最近更新済みならスキップ
            if th.theater_shops.filter(fetched_at__gte=cutoff,
                                       shop__sponsor_tier='free').exists():
                continue

            places = fetch_places(th.lat, th.lng, api_key)

            # free レコードを一括削除してフルリフレッシュ
            TheaterShop.objects.filter(theater=th,
                                       shop__sponsor_tier='free').delete()

            for p in places:
                shop, _ = Shop.objects.update_or_create(
                    name = p['name'],
                    lat  = p['geometry']['location']['lat'],
                    lng  = p['geometry']['location']['lng'],
                    defaults = dict(
                        category = p['types'][0],
                        rating   = p.get('rating'),
                        address  = p.get('vicinity', ''),
                        map_url=(
                            'https://www.google.com/maps/search/'
                            '?api=1'
                            f'&query={urllib.parse.quote_plus(p["name"])}'            # ←★追加
                            f'&query_place_id={p["place_id"]}'                        # ←★そのまま
                        ),
                        photo_url = (
                            f'https://maps.googleapis.com/maps/api/place/photo'
                            f'?maxwidth=400'
                            f'&photo_reference={p["photos"][0]["photo_reference"]}'
                            f'&key={api_key}'
                        ) if p.get('photos') else ''
                    )
                )
                TheaterShop.objects.update_or_create(
                    theater = th,
                    shop    = shop,
                    defaults = {
                        'distance_m': int(haversine(
                            th.lat, th.lng,
                            shop.lat, shop.lng
                        ))
                    }
                )

            self.stdout.write(self.style.SUCCESS(
                f'✓ {th.name}: {len(places)} shops updated'
            ))
