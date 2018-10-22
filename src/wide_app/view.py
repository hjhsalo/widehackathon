
import logging

from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


_logger = logging.getLogger(__name__)


def hello(request):
    _logger.info('hello called')
    return JsonResponse({'msg': 'hello'})


class IndexView(TemplateView):

    def get(self, request, **kwargs):
        _logger.info('index.html called')
        context = {
            'message': 'vilkommen!',
        }
        # note: django automatically searches templates from root directory templates/
        return render(request, 'index.html', context=context)
