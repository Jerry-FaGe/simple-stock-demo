from django.db import transaction
from django.db.utils import DatabaseError

from .models.good import Good
from .utils.cache import GoodCacheManager
from .exceptions import StockException, StockLockedError, CacheError, DatabaseError

class GoodReserveService:
    @transaction.atomic
    def reserve(self, good_id: int, count: int):
        """
        商品预定核心逻辑
        :param good_id: 商品 ID
        :param count: 数量
        :return:
        """
        try:
            # 使用数据库行级锁确保不会有并发问题
            good = Good.objects.select_for_update(nowait=True).get(id=good_id)

            if good.available_stock >= count:
                good.reserved += count
                good.save()

                # 失效缓存
                try:
                    GoodCacheManager.delete_detail(good_id)
                except Exception as e:
                    raise CacheError("缓存删除失败") from e

                return True, good.available_stock
            return False, good.available_stock

        except Good.DoesNotExist as e:
            raise StockException("商品不存在") from e
        except DatabaseError as e:
            # TODO 自动重试 或 提示用户失败
            raise StockLockedError("操作失败，请稍后重试") from e
        except Exception as e:
            raise StockException(f"系统异常: {e}") from e
