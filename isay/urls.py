from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import HomeTemplateView, Home2TemplateView, TeamTemplateView, ServicesTemplateView, NewsTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView, LoginTemplateView, SignupTemplateView, profile, modify_profile, ResetPasswordView
from isay import views

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("index/", Home2TemplateView.as_view(), name = "home2"),
    path("team/", TeamTemplateView.as_view(), name = "team"),
    path("services/", ServicesTemplateView.as_view(), name = "services"),
    path("news/", NewsTemplateView.as_view(), name = "news"),                ####HOMEPAGE
    path("make-an-appointment/", AppointmentTemplateView.as_view(), name="appointment"),
    path("manage-appointments/", ManageAppointmentTemplateView.as_view(), name="manage"),
    path('signup/', SignupTemplateView.as_view(), name='signup'),
    path('profile/',profile, name ="profile"),
    path('modify_profile/',modify_profile, name ="modify_profile"),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),  #forget password
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
