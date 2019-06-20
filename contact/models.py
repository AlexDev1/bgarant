from datetime import date

from django.db import models
from django.forms import widgets
from django.http import JsonResponse
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel
)
from wagtail.admin.utils import send_mail
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.core.fields import RichTextField
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )


class ContactPage(WagtailCaptchaEmailForm):
    template = "contact/contact_page.html"
    subpage_types = []
    parent_page_types = ['home.HomePage']
    max_count = 1
    # This is the default path.
    # If ignored, Wagtail adds _landing.html to your template name
    # landing_page_template = "contact/contact_page_landing.html"
    # ajax_template = "contact/contact_page_landing.html"
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('form_fields', label='Form Fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel("subject"),
        ], heading="Email Settings"),
    ]

    class Meta:
        verbose_name = "Страница контактов"

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self, user=request.user)

            if form.is_valid():
                self.process_form_submission(form)

                # Update the original landing page context with other data
                landing_page_context = self.get_context(request)
                landing_page_context['name'] = form.cleaned_data['name']

                return JsonResponse({
                    'response': 'success',
                })
        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context['form'] = form
        return render(
            request,
            self.get_template(request),
            context
        )

    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(',')]
        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field.label, value))
        submitted_date_str = date.today().strftime('%x')
        content.append('{}: {}'.format(
            'Отправлено', submitted_date_str))

        content = '\n'.join(content)
        subject = self.subject + " - " + submitted_date_str
        send_mail(subject, content, addresses, self.from_address)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # form = super(AbstractEmailForm, self).get_form(*args, **kwargs)  # use this syntax for Python 2.x
        # iterate through the fields in the generated form
        for name, field in form.fields.items():
            # here we want to adjust the widgets on each field
            # if the field is a TextArea - adjust the rows
            if isinstance(field.widget, widgets.Textarea):
                field.widget.attrs.update({'rows': '5'})
            # for all fields, get any existing CSS classes and add 'form-control'
            # ensure the 'class' attribute is a string of classes with spaces
            css_classes = field.widget.attrs.get('class', '').split()
            css_classes.append('form-control')
            field.widget.attrs.update({'class': ' '.join(css_classes)})
        return form
