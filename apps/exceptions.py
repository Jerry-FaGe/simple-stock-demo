from rest_framework import status
from rest_framework.exceptions import APIException


class StockException(APIException):
    """库存模块基础异常"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = '库存操作异常'
    default_code = 'stock_error'

class StockNotEnough(StockException):
    """库存不足异常"""
    status_code = status.HTTP_409_CONFLICT
    default_detail = '库存不足异常'
    default_code = 'stock_not_enough'

class StockLockedError(StockException):
    """库存锁定异常"""
    pass

class CacheError(APIException):
    """缓存异常"""
    pass

class DatabaseError(APIException):
    """数据库异常"""
    pass
