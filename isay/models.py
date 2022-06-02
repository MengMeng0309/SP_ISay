from django.db import models
from django.http import request
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


class Appointment(models.Model):
    SERVICES_CHOICES = (
        ('Counseling', 'Counseling'),
        ('Psychological Testing', 'Psychological Testing'),
        ('Career Guidance, Graduate Placement and Follow-up', 'Career Guidance, Graduate Placement and Follow-up'),
        ('Human Development Services', 'Human Development Services'),
        ('Peer Facilitating Program', 'Peer Facilitating Program'),
    )

    COLLEGE = (
        ('CAS', 'CAS'),
        ('CM', 'CM'),
        ('SOTECH', 'SOTECH'),
        ('CFOS', 'CFOS'),
        ('UPVHS', 'UPVHS'),
        ('UPVTC', 'UPVTC'),
    )

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    services = models.CharField(max_length=100,choices=SERVICES_CHOICES)
    college = models.CharField(max_length=100,choices=COLLEGE)
    gender = models.CharField(max_length=100,choices=GENDER)
    phone = models.CharField(max_length=12)
    request = models.TextField(blank=True)
    sent_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    who_accepted_f = models.CharField(max_length=50, blank= True)
    who_accepted_l = models.CharField(max_length=50, blank= True)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ["-sent_date"]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='teaMember.png', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 200 or img.width > 200:
            new_img = (200, 200)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    has_unread = models.BooleanField(default=False)

class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
