from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from isay.views import LoginTemplateView,ChangePasswordView  
from isay.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("isay.urls")),
    path('login/', LoginTemplateView.as_view(redirect_authenticated_user=True, template_name='login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
