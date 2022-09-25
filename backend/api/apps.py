from django.apps import AppConfig
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        pdfmetrics.registerFont(TTFont('Montserrat', settings.BASE_FONT))
