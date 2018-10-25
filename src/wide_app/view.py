
from functools import wraps
import json
import logging

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.shortcuts import render
import requests


_logger = logging.getLogger(__name__)


def handle_errors():
    """
    A decorator which catches all unhandled exceptions, wraps the error message
    into a json http response, and returns it to the client.
    """
    def catch_errors(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return JsonResponse({ 'message': str(e) }, status=500)
        return func_wrapper
    return catch_errors


def _get_keywords_from_annif(payload):
    try:
        response = requests.post('https://annif.fi/what', json={ 'data': payload })
    except:
        _logger.exception('Could not connect to annif')
        raise Exception('Could not connect to annif')

    if response.status_code != 200:
        _logger.warning('Annif returned error code: %d' % response.status_code)
        _logger.warning('Message: %s' % response.context)
        raise Exception('Annif returned an error: %s' % response.content)

    try:
        keywords = response.json()
    except:
        _logger.exception('Could not parse json from annif response')
        raise Exception('Error occurred while parsing annif response')

    return keywords


def _search_datasets(keywords):
    pass


@handle_errors()
@require_http_methods(["GET"])
def hello(request):
    _logger.info('-- hello called --')
    return JsonResponse({'msg': 'hello'})


@handle_errors()
@require_http_methods(["POST"])
def scrape(request):
    _logger.info('-- scrape called --')

    if not request.body:
        # body content is b'', i.e. empty string
        return JsonResponse({ 'keywords': [] })

    try:
        request_data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({ 'message': 'Received data is not valid json' }, status=500)

    # keywords = _get_keywords_from_annif(request_data)

    keywords = [
        'heijakkaa',
        'hoijakkaa',
    ]

    return JsonResponse({ 'keywords': keywords })


@handle_errors()
@require_http_methods(["POST"])
def search(request):
    _logger.info('-- search called --')

    if not request.body:
        # body content is b'', i.e. empty string
        return JsonResponse({ 'results': [] })

    try:
        request_data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({ 'message': 'Received data is not valid json' }, status=500)

    # results = _search_datasets(request_data)

    results = [
        { 'url': 'https://www.csc.fi', 'score': 42, 'other...': 'usefull stuff?' },
        { 'url': 'https://www.cern.ch', 'score': 42, 'other...': 'usefull stuff?' },
    ]

    return JsonResponse({ 'results': results })



class IndexView(TemplateView):

    def get(self, request, **kwargs):
        _logger.info('index.html called')
        context = {
            'message': 'vilkommen!',
        }
        # note: django automatically searches templates from root directory templates/
        return render(request, 'index.html', context=context)
