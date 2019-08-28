from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.blocks import RichTextBlock
from wagtail.core.fields import RichTextField, StreamField

from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from streams.blocks import BaseStreamBlock


class HomePage(Page):
    template = 'home/home.html'
    max_count = 1
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, verbose_name="Картинка",
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Только в ландшафтном режиме; горизонтальная ширина от 1000 до 3000 пикселей.')
    intro = models.CharField("Подзаголовок",
                             blank=True,
                             default="Заголовок",
                             max_length=50,
                             )
    text_intro = RichTextField("Текст под заголовком",
                             blank=True,
                             default="",
                             max_length=250,
                             )
    title_contacts = models.CharField("Подзаголовок Контактов",
                             blank=True,
                             default="Наши контакты",
                             max_length=50,
                             )
    text_contacts = RichTextField("Текст под заголовком а контактах",
                               blank=True,
                               default="",
                               max_length=250,
                               )
    youtube = models.URLField("Ссылка на Youtube-video")
    body = StreamField(BaseStreamBlock(), verbose_name="Содержимое страницы", blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('image'),
        FieldPanel('text_intro'),
        FieldPanel("youtube"),
        StreamFieldPanel('body'),
        FieldPanel('text_contacts'),

    ]

    subpage_types = [
        'contact.ContactPage',
    ]

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"
