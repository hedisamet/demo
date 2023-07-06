from django.contrib import admin
from django.urls import path
from events import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'events'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('admin/', views.AdminPage, name='admin'),
    # URL pattern for approving user creation with activation checkbox
    path('approve/<str:token>/', views.approve_user_creation, name='approve_user_creation'),
    path('delete/<int:user_creation_id>/', views.delete_user_creation, name='delete_user_creation'),
    path('signup/confirmation/', views.SignupConfirmationPage, name='signup_confirmation'),
    path('', views.index, name='index'),
    path('event.html', views.event, name='event'),
    path('event_details.html', views.event_details, name='event_details'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
