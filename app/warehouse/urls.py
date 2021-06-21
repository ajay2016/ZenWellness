from django.urls import path
from .views import (
    ProductCategoryList, ProductCategoryCreate, ProductCategoryUpdate,
    ProductCategoryDelete, ProductSubCategoryList, ProductSubCategoryCreate,
    ProductSubCategoryUpdate, ProductSubCategoryDelete, ProductList,
    ProductCreate, ProductUpdate, ProductDelete, WareHouseList,
    WareHouseCreate, WareHouseUpdate, WarehouseDelete, WarehouseProductList,
    WarehouseTransactionList, WarehouseTransactionCreate, 
    WarehouseTransactionUpdate, WarehouseTransactionDelete
)

app_name = 'warehouse'

urlpatterns = [
    path('product-category/', ProductCategoryList.as_view(), name='product_category_list'),
    path('product-category/create/', ProductCategoryCreate.as_view(), name='product_category_add'),
    path('product-category/update/<slug>', ProductCategoryUpdate.as_view(), name='product_category_update'),
    path('product-category/delete/<slug>', ProductCategoryDelete.as_view(), name='product_category_delete'),
    path('product-sub-category/', ProductSubCategoryList.as_view(), name='product_subcategory_list'),
    path('product-sub-category/create/', ProductSubCategoryCreate.as_view(), name='product_subcategory_add'),
    path('product-sub-category/update/<slug>', ProductSubCategoryUpdate.as_view(), name='product_subcategory_update'),
    path('product-sub-category/delete/<slug>', ProductSubCategoryDelete.as_view(), name='product_subcategory_delete'),
    path('product/', ProductList.as_view(), name="product_list"),
    path('product/create/', ProductCreate.as_view(), name="product_add"),
    path('product/update/<slug>', ProductUpdate.as_view(), name="product_update"),
    path('product/delete/<slug>', ProductDelete.as_view(), name="product_delete"),
    path('warehouse/', WareHouseList.as_view(), name="warehouse_list"),
    path('warehouse/create/', WareHouseCreate.as_view(), name="warehouse_add"),
    path('warehouse/update/<slug>', WareHouseUpdate.as_view(), name="warehouse_update"),
    path('warehouse/delete/<slug>', WarehouseDelete.as_view(), name="warehouse_delete"),
    path('warehouse/products/<slug>', WarehouseProductList.as_view(), name="warehouse_product_list"),
    path('warehouse/transaction/<slug>', WarehouseTransactionList.as_view(), name="warehouse_transaction"),
    path('warehouse/transaction/<slug>/add', WarehouseTransactionCreate.as_view(), name="warehouse_transaction_add"),
    path('warehouse/transaction/<str:warehouse>/update/<pk>', WarehouseTransactionUpdate.as_view(), name="warehouse_transaction_update"),
    path('warehouse/transaction/<str:warehouse>/delete/<pk>', WarehouseTransactionDelete.as_view(), name="warehouse_transaction_delete")
]
