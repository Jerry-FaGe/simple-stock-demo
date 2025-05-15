from django.urls import path

from .views import GoodListView, GoodDetailView, GoodReserveView


urlpatterns = [
    path('good/', GoodListView.as_view(), name='good_list'),
    path("good/<int:pk>/", GoodDetailView.as_view(), name="good_detail"),
    path("good/<int:pk>/reserve/", GoodReserveView.as_view(), name="good_reserve")
]
