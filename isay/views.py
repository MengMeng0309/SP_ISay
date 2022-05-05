from email.message import Message
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from .models import Appointment
from django.views import View
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from .forms import RegisterForm,LoginForm,UpdateUserForm, UpdateProfileForm

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

class SignupTemplateView(TemplateView):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'signup.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(SignupTemplateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})

class TeamTemplateView(TemplateView):
    template_name = "team.html"

class ServicesTemplateView(TemplateView):
    template_name = "services.html"

class NewsTemplateView(TemplateView):
    template_name = "news.html"

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
    login_required = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({
            "appointments": appointments,
            "title": "Manage Appointments"
        })
        return context

class LoginTemplateView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(LoginTemplateView, self).form_valid(form)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')

class ModifyProfileTemplateView(TemplateView):
    template_name = "modify_profile.html"
