from django.urls import path
from . import views

urlpatterns = [
    # Nutritional Information
    path('nutritional-info/',
         views.NutritionalInformationListView.as_view(),
         name='nutritionalinformation-list'
         ),
    path('nutritional-info/add/',
         views.NutritionalInformationCreateView.as_view(),
         name='nutritionalinformation-add'
         ),
    path('nutritional-info/<int:pk>/',
         views.NutritionalInformationDetailView.as_view(),
         name='nutritionalinformation-detail'
         ),
    path('nutritional-info/<int:pk>/edit/',
         views.NutritionalInformationUpdateView.as_view(),
         name='nutritionalinformation-edit'
         ),
    path('nutritional-info/<int:pk>/delete/',
         views.NutritionalInformationDeleteView.as_view(),
         name='nutritionalinformation-delete'
         ),

    # Products
    path('products/',
         views.ProductListView.as_view(),
         name='product-list'
         ),
    path('products/add/',
         views.ProductCreateView.as_view(),
         name='product-add'
         ),
    path('products/<int:pk>/',
         views.ProductDetailView.as_view(),
         name='product-detail'
         ),
    path('products/<int:pk>/edit/',
         views.ProductUpdateView.as_view(),
         name='product-edit'
         ),
    path('products/<int:pk>/delete/', 
         views.ProductDeleteView.as_view(), 
         name='product-delete'
         ),
    path(
        'products/<int:pk>/nutritional-values/',
        views.ProductNutritionalValuesUpdateView.as_view(),
        name="product-nutritional-values-update",
    ),
]
