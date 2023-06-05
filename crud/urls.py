from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin.site.urls),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('items/', views.items, name='items'),
]