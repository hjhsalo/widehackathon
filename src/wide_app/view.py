
from functools import wraps
import json
import logging

from annif_client import AnnifClient
from finna_client import FinnaClient
from django.http import JsonResponse
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
    annif = AnnifClient()
    try:
        results = annif.analyze(project_id='yso-en', text="The quick brown fox", limit=5)
    except:
        _logger.exception('Could not connect to annif')
        raise Exception('Could not connect to annif')

    keywords = [row['label'] for row in results]
    return keywords


def _search_datasets(keywords):
    finna = FinnaClient()
    results = finna.search(', '.join(keywords), limit=5)
    return results


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
        request_data = json.loads(request.body.decode('utf-8'))
    except:
        return JsonResponse({ 'message': 'Received data is not valid json' }, status=500)

    keywords = _get_keywords_from_annif(request_data)

    return JsonResponse({ 'keywords': keywords })


@handle_errors()
@require_http_methods(["POST"])
def search(request):
    _logger.info('-- search called --')

    if not request.body:
        # body content is b'', i.e. empty string
        return JsonResponse({ 'results': [] })

    try:
        request_data = json.loads(request.body.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return JsonResponse({ 'message': 'Received data is not valid json' }, status=500)

    # import ipdb; ipdb.set_trace()
    results = _search_datasets(request_data)
    from pprint import pprint
    pprint(results)

    return JsonResponse({ 'results': results })


class IndexView(TemplateView):

    def get(self, request, **kwargs):
        _logger.info('index.html called')
        context = {
            'message': 'vilkommen!',
        }
        # note: django automatically searches templates from root directory templates/
        return render(request, 'index.html', context=context)
