# 小型库存预订模块

基于 Django + PostgreSQL + Redis 的简单库存预订系统。

## 项目介绍

使用 Django 编写的库存预订系统 Demo，属于 Restful API 后端项目，附带前端只用于简单的功能展示。
使用索引优化数据库查询，通过事务以及 select_for_update 行级锁确保库存原子性以及避免超卖问题。
使用 Redis 缓存查询参数及结果，通过 Django Signals 自动清理相关缓存。

## 主要 API

- 商品列表查询
   - GET /api/good/

- 商品名称搜索
   - GET /api/good/?name=商品名称

- 商品详情查询
   - GET /api/good/{id}/

- 商品预订
   - POST /api/good/{id}/reserve/

## 项目结构

```
SimpleStockDemo/
├── apps/
│   ├── models/         # 数据模型层
│   ├── serializers/    # 序列化层
│   ├── services/       # 业务服务层
│   ├── utils/         # 工具类
│   │   └── cache.py   # 缓存管理
│   ├── signals/       # 信号处理
│   └── views.py       # 视图控制层
├── templates/         # 前端模板
└── SimpleStockDemo/   # 项目配置
```
