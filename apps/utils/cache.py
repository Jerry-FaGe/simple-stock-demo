import redis
from hashlib import md5

from django.conf import settings
from django.core.cache import cache


class GoodCacheManager:
    @staticmethod
    def generate_cache_key(prefix, params):
        """键名 MD5 化防止特殊字符"""
        param_str = md5(str(sorted(params.items())).encode()).hexdigest()
        return f"{prefix}:{param_str}"

    @classmethod
    def get_list(cls, params):
        key = cls.generate_cache_key("good_list", params)
        return cache.get(key)

    @classmethod
    def set_list(cls, params, data, timeout=1200):
        key = cls.generate_cache_key("good_list", params)
        cache.set(key, data, timeout)

    @staticmethod
    def delete_list(prefix="good_list") -> int:
        r = redis.Redis.from_url(settings.CACHES["default"]["LOCATION"])
        to_delete = list(r.scan_iter(match=f"*{prefix}*", count=1000))
        if to_delete:
            return r.delete(*to_delete)
        return 0

    @staticmethod
    def get_detail(good_id):
        return cache.get(f"good_detail:{good_id}")

    @staticmethod
    def set_detail(good_id, data, timeout=1200):
        cache.set(f"good_detail:{good_id}", data, timeout)

    @staticmethod
    def delete_detail(good_id):
        cache.delete(f"good_detail:{good_id}")

    @staticmethod
    def set_null_detail(good_id, timeout=60):
        cache.set(f"good_detail:{good_id}", b"__NULL__", timeout)

    @staticmethod
    def is_null_cache(data):
        return data == b"__NULL__"
