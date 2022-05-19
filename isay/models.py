from django.db import models
from django.http import request
from django.contrib.auth.models import User
from PIL import Image

class Appointment(models.Model):
    # SERVICES_CHOICES = (
    #     ('C', 'Counseling'),
    #     ('T', 'Psychological Testing'),
    #     ('F', 'Career Guidance, Graduate Placement and Follow-up'),
    #     ('H', 'Human Development Services'),
    #     ('P', 'Peer Facilitating Program'),
    # )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    # services = models.CharField(max_length=1, choices=SERVICES_CHOICES)
    phone = models.CharField(max_length=50)
    request = models.TextField(blank=True)
    sent_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
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

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)