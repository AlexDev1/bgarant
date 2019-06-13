from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField

from wagtail.core.models import Page


class HomePage(Page):
    max_count = 1

    intro = models.CharField("Подзаголовок",
                             blank=True,
                             default="Заголовок",
                             max_length=50,
                             )
    text_intro = RichTextField("Текст под заголовком",
                             blank=True,
                             default="",
                             max_length=50,
                             )
    title_contacts = models.CharField("Подзаголовок Контактов",
                             blank=True,
                             default="Наши контакты",
                             max_length=50,
                             )
    text_contacts = RichTextField("Текст под заголовком а контактах",
                               blank=True,
                               default="",
                               max_length=50,
                               )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('text_intro'),
        # StreamFieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"
