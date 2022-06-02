import datetime
import json
import requests
from email.message import Message
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.template import Context
from django.template.loader import render_to_string, get_template



from .forms import RegisterForm,LoginForm,UpdateUserForm, UpdateProfileForm,ThreadForm,MessageForm
from .models import Appointment,User,ThreadModel,MessageModel


class HomeTemplateView(TemplateView):
    template_name = "index.html"
    model = User

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email = EmailMessage(
            subject = f"{name} from iSay Website.",
            body = message,
            from_email = settings.EMAIL_HOST_USER,
            to = [settings.EMAIL_HOST_USER],
            reply_to = [email]
        )
        email.send()
        
        messages.success(request, 'Email has been sucessfully sent!')
        return redirect(to='home')

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
            recaptcha_response = request.POST.get("g-recaptcha-response")
            check_url = "https://www.google.com/recaptcha/api/siteverify"
            secret = settings.RECAPTCHA_PRIVATE_KEY
            check_data = {"secret":secret, "response": recaptcha_response}
            check_response = requests.post(url = check_url, data = check_data)
            check_json = json.loads(check_response.text)

            if check_json['success'] == True:

                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}')
            else:
                messages.error(request, 'Invalid Captcha, Please try again')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})

class TeamTemplateView(TemplateView):
    template_name = "team.html"

class ServicesTemplateView(TemplateView):
    template_name = "services.html"

class NewsTemplateView(TemplateView):
    template_name = "news.html"

class SummaryTemplateView(TemplateView):
    template_name = "summary_page.html"

class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"
    def post(self, request):
        fname = request.user.first_name 
        lname = request.user.last_name 
        email = request.user.email 
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        services = request.POST.get("services")
        college = request.POST.get("college")
        message = request.POST.get("request")
        

        appointment = Appointment.objects.create(
            first_name=fname, # will carry the firstname from registration form 
            last_name=lname,
            email=email,
            phone=mobile,
            gender=gender,
            services=services,
            college=college,
            request=message,

           
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making an appointment, we will email you ASAP!")
        return HttpResponseRedirect(request.path)

class ManageAppointmentTemplateView(ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3

    def post(self, request):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        who_accepted_f = request.user.first_name
        who_accepted_l = request.user.last_name
        appointment = Appointment.objects.get(id = appointment_id)
        appointment.accepted = True
        appointment.who_accepted_f = who_accepted_f
        appointment.who_accepted_l = who_accepted_l
        appointment.accepted_date = datetime.datetime.now()
        appointment.save()

        data = {
            "fname":appointment.first_name,
            "wfname":appointment.who_accepted_f,
            "wlname":appointment.who_accepted_l,
            "date":date,
        }

        message = get_template('email.html').render(data)
        email = EmailMessage(
            "Appointment Confirmation in iSay",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
        )
        email.content_subtype = "html"
        email.send()

        messages.add_message(request, messages.SUCCESS, f"Appointment Accepted at {date}!")
        return HttpResponseRedirect(request.path)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({
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


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message = "We've emailed you instructions for resetting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')

#PROFILE PAGE
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})

#MODIFY PROFILE
@login_required
def modify_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'modify_profile.html', {'user_form': user_form, 'profile_form': profile_form})


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'chat/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')
        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            return redirect('create-thread')

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'chat/inbox.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )

        message.save()
        return redirect('thread', pk=pk)

class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'chat/thread.html', context)