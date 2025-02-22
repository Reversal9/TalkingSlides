from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('message/', views.get_message, name="get_message"),
    # path('upload/', views.upload_pdf, name='upload_pdf'),
    # path('view/<int:pdf_id>/', views.view_pdf, name='view_pdf'),
    # path('delete/<int:pdf_id>/', views.delete_pdf, name='delete_pdf'),
    # path("login/", views.login, name="login"),
    # path("logout/", views.logout, name="logout"),
    # path("callback/", views.callback, name="callback"),
]
