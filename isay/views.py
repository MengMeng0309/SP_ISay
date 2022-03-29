from email.message import Message
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from .models import Appointment

class HomeTemplateView(TemplateView):
    template_name = "index.html"

    # def post(self, request):
    #     name = request.POST.get("name")
    #     email = request.POST.get("email")
    #     message = request.POST.get("message")

    #     email = EmailMessage(
    #         subject = f"{name} from iSay Website.",
    #         body = message,
    #         from_email = settings.EMAIL_HOST_USER,
    #         to = [settings.EMAIL_HOST_USER],
    #         reply_to = [email]
    #     )
    #     email.send()
    #     return HttpResponse("Email sent successfully!")

class Home2TemplateView(TemplateView):
    template_name = "index.html"

class TeamTemplateView(TemplateView):
    template_name = "team.html"

class ServicesTemplateView(TemplateView):
    template_name = "services.html"

class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message,
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making an appointment, we will email you ASAP!")
        return HttpResponseRedirect(request.path)

class ManageAppointmentTemplateView(TemplateView):
    template_name = "manage-appointments.html"
    # login_required = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({
            "appointments": appointments,
            "title": "Manage Appointments"
        })
        return context

class LoginTemplateView(TemplateView):
    template_name = "login.html"

class SignupTemplateView(TemplateView):
    template_name = "signup.html"