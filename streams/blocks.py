"""Streamfields live in here."""

from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock,
    ListBlock, PageChooserBlock, URLBlock, StructValue)
from wagtail.core.blocks import StructBlock, StreamBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(StructBlock):
    """Название и текст и ничего больше."""

    title = CharBlock(required=True, help_text="Add your title")
    text = TextBlock(required=True, help_text="Add additional text")

    class Meta:  # noqa
        template = "layouts/title_and_text_block.html"
        icon = "edit"
        label = "Название и текст"


class SimpleCardBlock(StructBlock):
    """Карточки Картинкой и текстом."""

    title = CharBlock(label="Заголовок", required=True, help_text="Добавьте свой заголовок")
    text = CharBlock(label="Подзаголовок", required=True, help_text="Текст под заголовком")
    cards = ListBlock(
        StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", TextBlock(label="Заголовок", required=True, help_text="Добавьте Блока")),
                ("text", TextBlock(required=True, max_length=200)),

            ]
        )
    )

    class Meta:  # noqa
        template = "layouts/simple_card_block.html"
        icon = "placeholder"
        label = "Картинка и текст"


class CardBlock(StructBlock):
    """Карточки с изображением, текстом и кнопкой."""

    title = CharBlock(required=True, help_text="Add your title")

    cards = ListBlock(
        StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", CharBlock(required=True, max_length=40)),
                ("text", TextBlock(required=True, max_length=200)),
                ("button_page", PageChooserBlock(required=False)),
                (
                    "button_url",
                    URLBlock(
                        required=False,
                        help_text="Если выбрана страница кнопки выше, она будет использоваться первой.",  # noqa
                    ),
                ),
            ]
        )
    )

    class Meta:  # noqa
        template = "layouts/card_block.html"
        icon = "placeholder"
        label = "Карточка с фото"


class RichtextBlock(RichTextBlock):
    """Richtext со всеми функциями."""

    class Meta:  # noqa
        template = "layouts/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"


class SimpleRichtextBlock(RichTextBlock):
    """Richtext without (limited) all the features."""

    def __init__(
        self, required=True, help_text=None, editor="default", features=None, **kwargs
    ):  # noqa
        super().__init__(**kwargs)
        self.features = ["bold", "italic", "link"]

    class Meta:  # noqa
        template = "layouts/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"


class CTABlock(StructBlock):
    """Простой призыв к действию."""

    title = CharBlock(label="Заголовк", required=True, max_length=60)
    text = RichTextBlock(label="Текст", required=True, features=["bold", "italic"])
    button_page = PageChooserBlock(label="Страница", required=False)
    button_url = URLBlock(label="URL", required=False)
    button_text = CharBlock(label="Текст на кнопке", required=True, default='Узнать больше', max_length=40)

    class Meta:  # noqa
        template = "layouts/cta_block.html"
        icon = "placeholder"
        label = "Призыв к действию"


class LinkStructValue(StructValue):
    """Дополнительная логика для наших URL."""

    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url

        return None

    # def latest_posts(self):
    #     return BlogDetailPage.objects.live()[:3]


class ButtonBlock(StructBlock):
    """An external or internal URL."""

    button_page = PageChooserBlock(required=False, help_text='Если выбрано, этот URL будет использоваться первым')
    button_url = URLBlock(required=False, help_text='Если добавлено, этот URL будет использоваться вторично на странице кнопки')

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['latest_posts'] = BlogDetailPage.objects.live().public()[:3]
    #     return context

    class Meta:  # noqa
        template = "layouts/button_block.html"
        icon = "placeholder"
        label = "Одиночная кнопка"
        value_class = LinkStructValue


class ImageBlock(StructBlock):
    """
    Пользовательский `StructBlock` для использования изображений с соответствующими заголовками и
     атрибуция данных
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Пользовательский `StructBlock`, который позволяет пользователю выбирать размеры заголовков h2 - h4
    """
    heading_text = CharBlock(classname="title", required=True, label="Заголовок")
    size = ChoiceBlock(choices=[
        ('', 'Выберите размер заголовка'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False, label="Размер")

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"



class BlockQuote(StructBlock):
    """
    Пользовательский `StructBlock`, который позволяет пользователю приписывать цитату автору
    """
    text = TextBlock(label="Текст")
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Определите пользовательские блоки, которые StreamField будет использовать
    """
    heading_block = HeadingBlock(label="Заголовок")
    paragraph_block = RichTextBlock(label="Простой текст",
        icon="fa-paragraph",
        template="blocks/paragraph_block.html"
    )
    image_block = ImageBlock(label="Картинка")
    block_quote = BlockQuote(label="Цитата")
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")
