from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel


@register_setting
class ContactSettings(BaseSetting):
    """Настройки котактов."""
    logo = models.ForeignKey(
        "wagtailimages.Image", verbose_name="Логотип",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    name = models.CharField(verbose_name="Название", max_length=15)
    address = models.CharField(verbose_name="Адрес", max_length=200)
    phone = models.CharField(verbose_name="Телефон", max_length=15)
    email = models.CharField(verbose_name="Email", max_length=15)
    # header_text = models.CharField(verbose_name="Текст на верху страницы", max_length=75)
    # promo_text = models.CharField(verbose_name="Промо-текст с адресом", max_length=100)
    #
    # facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
    # instagram = models.URLField(blank=True, null=True, help_text="Instogram URL")
    # vk = models.URLField(blank=True, null=True, help_text="YouTube Channel URL")

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            FieldPanel("address"),
            FieldPanel("phone"),
            FieldPanel("email"),
            ImageChooserPanel('logo')
        ], heading="КОНТАКТЫ"),
    ]

    class Meta:
        verbose_name = "Настройки контактов"
