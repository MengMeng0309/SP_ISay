from django.urls import path
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView, LoginTemplateView, SignupTemplateView

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("make-an-appointment/", AppointmentTemplateView.as_view(), name="appointment"),
    path("manage-appointments/", ManageAppointmentTemplateView.as_view(), name="manage"),
    path("login/", LoginTemplateView.as_view(), name="login"),
    path("signup/", SignupTemplateView.as_view(), name="signup"),
]
