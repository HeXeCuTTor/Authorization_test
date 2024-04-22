from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django_rest_passwordreset.tokens import get_token_generator
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'phone'
    phone = models.CharField(max_length=22, blank=True, unique=True, verbose_name='Номер телефона')
    invited_by = models.PositiveIntegerField(null=True, verbose_name="ID пригласившего")

    def __str__(self):
        return f'{self.username}'    


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name = 'Список пользователей'
        ordering = ('-phone',)

class Invite(models.Model):
    code = models.CharField(max_length=6, unique=True, verbose_name="Значение")
    user = models.OneToOneField(User, verbose_name='Пользователь', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Инвайт код'
        verbose_name_plural = "Инвайт коды"
        ordering = ('-code',)

    def __str__(self):
        return self.code

class SendCode(models.Model):
    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'

    @staticmethod
    def generate_key():
        return get_token_generator().generate_token()

    user = models.ForeignKey(
        User,
        related_name='confirm_code',
        on_delete=models.CASCADE,
        verbose_name=_("The User which is associated to this code")
    )

    key = models.CharField(
        _("Key"),
        max_length=64,
        db_index=True,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(SendCode, self).save(*args, **kwargs)

    def __str__(self):
        return "Confirm code for user {user}".format(user=self.user)
