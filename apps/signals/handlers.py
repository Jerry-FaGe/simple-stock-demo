from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from ..models import Good
from ..utils.cache import GoodCacheManager


@receiver([post_save, post_delete], sender=Good)
def handle_good_cache_invalidation(sender, instance, **kwargs):
    # 失效单商品缓存
    GoodCacheManager.delete_detail(instance.id)

    # TODO 待优化，正常项目需要更精细的控制
    # 失效所有列表缓存
    GoodCacheManager.delete_list()
