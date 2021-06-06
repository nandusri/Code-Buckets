import os
import uuid
from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import FileExtensionValidator


class User(AbstractUser, TimeStampedModel):
    contact = models.CharField(max_length=100, blank = True, null = True)
    profile_picture = models.ImageField(upload_to='images', null = True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png','jpeg','jpg'])])
    is_active = models.BooleanField(_('active'), default=True)
    
    def __str__(self):
        return self.email
User._meta.get_field('email').blank = False
User._meta.get_field('email')._unique = True