from django.db import models
from django.contrib.auth.models import AbstractUser
ORDINARY_USER, ADMIN, MANAGER = ('ordinary_manager','admin', 'manager')
NEW, CODE_VERIFY, DONE, PHOTO_DONE = ('new', 'code_verify', 'done', 'photo_done')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')
from django.core.validators import FileExtensionValidator
from baseapp.models import BaseModel
from datetime import timedelta, datetime
from conf.settings import EMAIL_EXPIRATION_TIME, PHONE_EXPIRATION_TIME
import random
# Create your models here.


class CumtomUser(AbstractUser, BaseModel):
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
        (ADMIN, ADMIN),
        (MANAGER, MANAGER)
    )
    
    USER_STATUS = (
        (NEW, NEW),
        (CODE_VERIFY, CODE_VERIFY),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE)
    )
    
    USER_AUTH_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default=ORDINARY_USER)
    
    user_role_type = models.CharField(max_length=25, choices=USER_AUTH_TYPE)
    
    user_status = models.CharField(max_length=25, choices=USER_STATUS, default=NEW)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True, unique=True)
    photo = models.ImageField(upload_to='users/', validators=FileExtensionValidator(allowed_extensions=['jpg', 'png', 'heic']))
    
    
    
        
    
    
    def __str__(self):
        return self.username
    
    
    
    
    def create_code(self, verify_type):
        code = ''.join([str(random.randint(1000)) [-1] for _ in range(4)])
        
        
        CodeVerify.objects.create(
            user = self,
            verify_type = verify_type,
            code = code
        )
        
        return code
    
    
    def check_username(self):
        pass
    
    def check_email(self):
        pass
    
    def hash_password(self):
        pass
    
    def token(self):
        pass
    
    def clean(self):
        pass
    
    
    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        return super().save(force_insert, force_update, using, update_fields)
    
    
    
    
        
        
        
    
    
    
class CodeVerify(BaseModel):
    VERIFY_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
        
    )
    
    code = models.CharField(max_length=4, blank=True, null=True)
    user = models.ForeignKey(CumtomUser, on_delete=models.CASCADE, related_name='code')
    verify_type = models.CharField(max_length=20, choices=VERIFY_TYPE)
    is_active = models.BooleanField(default=False)
    exparation_time = models.DateTimeField()
    
    
    def __str__(self):
        return f"{self.user.username} | {self.code}"
    
    
    
        
    
    
    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.exparation_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRATION_TIME)
        else:
            self.exparation_time = datetime.now() + timedelta(minutes=PHONE_EXPIRATION_TIME)
        super().save()
        
        
        
    
    
    
    
    