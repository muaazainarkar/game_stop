from django.urls import path
from gamestopapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    path('create_product',views.create_product),
    path('register',views.user_register),
    path('read',views.read),
    path('update/<rid>',views.update),
    path('delete/<rid>', views.delete_product),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('add_to_cart/<rid>',views.create_cart),
    path('read_cart', views.read_cart),
    path('delete_cart/<rid>',views.delete_cart),
    path('update_cart/<rid>/<q>',views.update_cart),
    path('orders/<rid>',views.create_orders),
    path('read_orders',views.read_orders),
    path('review_orders/<rid>', views.create_review),
    path('product_detail/<rid>',views.read_product_details),
    path('forgot_password',views.forget_password),
    path('otp_verify',views.otp_verify),
    path('new_password',views.new_password)
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)