import logging

from django.http import HttpResponse
from django.views.generic import TemplateView

# Get an instance of a logger
logger = logging.getLogger(__name__)


class HomePageView(TemplateView):
    template_name = 'home.html'


def LoggingExampleView(request):
    # Log a simple string message
    logger.info('This is an info message from LoggingExampleView')

    # Log a dictionary
    logger.info({'user': 'admin', 'action': 'login', 'status': 'success'})

    # Log a list
    logger.info(['User logged in', 'admin', 'success'])

    return HttpResponse("Check your logs for messages.")
