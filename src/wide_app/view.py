
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


# truncate abstracts longer than this
ABSTRACT_MAX_LEN = 200


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
        results = annif.analyze(project_id='yso-en', text=payload, limit=5)
    except:
        _logger.exception('Could not connect to annif')
        raise Exception('Could not connect to annif')

    keywords = [row['label'] for row in results]
    return keywords


def _search_datasets(keywords):
    # finna = FinnaClient()
    # results = finna.search(', '.join(keywords), limit=5)
    # query = 'bibjson.journal.title:"Journal of Science"'

    # keywords = ['mathematics']
    results = []
    queries = [
        'bibjson.keywords:"%s"',
        'bibjson.abstract:"%s"',
        # more interesting fields ?
        # https://doaj.org/api/v1/docs#!/Search/get_api_v1_search_articles_search_query
    ]

    # results can have same dataset multiple times due to stupid way of making multiple queries.
    # AND clause does not seem to work, while OR does work. example:
    # WORKS
    # response = requests.get('https://doaj.org/api/v1/search/articles/bibjson.abstract:"mathematics" OR bibjson.year="1999"')
    # NOT WORKS
    # response = requests.get('https://doaj.org/api/v1/search/articles/bibjson.abstract:"mathematics" AND bibjson.year="1999"')
    # opportunity for some manual "scoring" of results, or figuring out how to query doaj better...

    for kw in keywords:
        for query_template in queries:
            query = query_template % kw
            response = requests.get('https://doaj.org/api/v1/search/articles/%s?pageSize=10' % query)
            results.extend(response.json()['results'])

    with open('out', 'w') as f:
        import json
        json.dump(results, f)

    processed_results = []

    for res in results:
        abstract = res['bibjson'].get('abstract', 'n/a')
        processed_results.append({
            'title': res['bibjson']['title'],
            'abstract': abstract if len(abstract) < ABSTRACT_MAX_LEN else '%s...' % abstract[:ABSTRACT_MAX_LEN],
            'links': [ l['url'] for l in res['bibjson']['link'] ],
        })

    # filter/priorize duplicates here

    return processed_results


# @handle_errors()
@require_http_methods(["GET"])
def hello(request):
    _logger.info('-- hello called --')
    return JsonResponse({'msg': 'hello'})


# @handle_errors()
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

    keywords = _get_keywords_from_annif(request_data['content'])

    return JsonResponse({ 'keywords': keywords })


# @handle_errors()
@require_http_methods(["POST"])
def search(request):
    _logger.info('-- search called --')

    if not request.body:
        # body content is b'', i.e. empty string
        return JsonResponse({ 'results': [] })

    # try:
    request_data = json.loads(request.body.decode('utf-8'))
    # except json.decoder.JSONDecodeError:
        # return JsonResponse({ 'message': 'Received data is not valid json' }, status=500)

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
