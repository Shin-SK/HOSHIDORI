# core/management/commands/update_news.py
import re, html
import feedparser, requests, pytz, traceback
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import News

# ───────── 設定 ─────────
FEEDS = {
    "ローチケ演劇宣言": "https://engekisengen.com/feed/",
    "SPICE"  : "https://spice-api.eplus.jp/rss/articles/3/latest.xml?encoded=1",
}
KEEP_DAYS = 30        # これより古い記事は削除
MAX_LEN   = 500       # title / image 等の max_length

# ───────── helpers ─────────
def safe(text, limit=MAX_LEN):
    """DB 文字数制限オーバーで落ちないように切り詰める"""
    return (text or "")[: limit]

IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)')

def pick_thumb(entry):
    # ①  media:thumbnail / media:content
    media = entry.get("media_thumbnail") or entry.get("media_content")
    if media and isinstance(media, list):
        return media[0].get("url", "")

    # ②  enclosure
    if entry.get("enclosures"):
        return entry.enclosures[0].get("url", "")

    # ③  content:encoded 内の <img src="...">
    html_content = (
        entry.get("content", [{}])[0].get("value")  # feedparser がここに入れる
        or entry.get("content_encoded")             # 念のため
        or entry.get("description", "")
    )
    if html_content:
        # HTML エンティティを戻して img src を抜く
        m = IMG_RE.search(html.unescape(html_content))
        if m:
            return m.group(1)

    # ④ それでも無ければ空文字
    return ""


# ───────── コマンド本体 ─────────
class Command(BaseCommand):
    help = "舞台系 RSS を取り込んで News テーブルを更新（デバッグ版）"

    def handle(self, *args, **opts):
        v = int(opts.get("verbosity", 1))
        created_cnt = updated_cnt = skipped_cnt = err_cnt = 0

        for src, url in FEEDS.items():
            if v:
                self.stdout.write(f"▼ feed: {src}  ({url})")

            feed = feedparser.parse(url)
            if v:
                self.stdout.write(f"  entries = {len(feed.entries)}")

            for e in feed.entries:
                try:
                    # ----- 公開日時 -----
                    if hasattr(e, "published_parsed") and e.published_parsed:
                        pub = datetime(*e.published_parsed[:6], tzinfo=pytz.UTC)
                    else:
                        if v >= 2:
                            self.stdout.write("  - no pubdate, use now   ", e.link)
                        pub = timezone.now()

                    # ----- 重複チェック -----
                    obj, created = News.objects.update_or_create(
                        link=e.link,
                        defaults=dict(
                            title  = safe(e.title),
                            source = src,
                            pub_at = pub,
                            image  = safe(pick_thumb(e)),
                        ),
                    )
                    if created:
                        created_cnt += 1
                        if v >= 3:
                            self.stdout.write("  + saved:", obj.title)
                    else:
                        updated_cnt += 1
                        if v >= 3:
                            self.stdout.write("  = updated:", obj.title)

                except Exception as exc:
                    err_cnt += 1
                    if v:
                        self.stdout.write(
                            self.style.WARNING(
                                f"  ! err: {exc.__class__.__name__}: {exc}"
                            )
                        )
                        if v >= 3:
                            traceback.print_exc()

        # ----- 古い記事を掃除 -----
        old_qs = News.objects.filter(pub_at__lt=timezone.now() - timedelta(days=KEEP_DAYS))
        deleted_cnt, _ = old_qs.delete()

        # ----- サマリ -----
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ News updated  (+{created_cnt} / ={updated_cnt} / "
                f"-{deleted_cnt} del / !{err_cnt} err / {skipped_cnt} skip)"
            )
        )
