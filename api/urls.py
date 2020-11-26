from django.urls import path
from .views import ProductList, ProductCreate, ProductDestroy, ProductUpdate, ProductRetrieveUpdateDestroy

urlpatterns = [
    path('v1/', ProductList.as_view(), name='api-home'),
    path('v1/create/', ProductCreate.as_view(), name='create'),
    path('v1/delete/<int:id>/', ProductDestroy.as_view(), name='delete'),
    # path('v1/update/<int:id>/', ProductUpdate.as_view(), name='update'),
    path('v1/update/<int:id>/', ProductRetrieveUpdateDestroy.as_view(), name='update'),

   
]