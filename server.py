import json
import os
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

PRICING_FILE = 'pricing.json'
QUOTES_FILE = 'quotes.json'


def load_pricing():
    with open(PRICING_FILE, 'r') as f:
        return json.load(f)


def load_quotes():
    if not os.path.exists(QUOTES_FILE):
        return []
    with open(QUOTES_FILE, 'r') as f:
        return json.load(f)


def save_quotes(quotes):
    with open(QUOTES_FILE, 'w') as f:
        json.dump(quotes, f, indent=2)


def create_quote(data):
    quotes = load_quotes()
    quote_id = len(quotes) + 1
    quote = {
        'id': quote_id,
        'customer': data.get('customer', 'Unknown'),
        'items': data.get('items', []),
        'status': 'draft'
    }
    quotes.append(quote)
    save_quotes(quotes)
    return quote


def update_quote_status(quote_id, status):
    quotes = load_quotes()
    for q in quotes:
        if q['id'] == quote_id:
            q['status'] = status
            save_quotes(quotes)
            return q
    return None


def application(environ, start_response):
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', 'GET')
    if path == '/pricing' and method == 'GET':
        data = json.dumps(load_pricing()).encode()
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [data]
    elif path == '/quote' and method == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError, TypeError):
            size = 0
        body = environ['wsgi.input'].read(size)
        data = json.loads(body.decode() or '{}')
        quote = create_quote(data)
        start_response('201 Created', [('Content-Type', 'application/json')])
        return [json.dumps(quote).encode()]
    elif path.startswith('/quote/') and method == 'GET':
        quote_id = int(path.split('/')[-1])
        quotes = load_quotes()
        for q in quotes:
            if q['id'] == quote_id:
                start_response('200 OK', [('Content-Type', 'application/json')])
                return [json.dumps(q).encode()]
        start_response('404 Not Found', [('Content-Type', 'application/json')])
        return [json.dumps({'error': 'Quote not found'}).encode()]
    elif path.startswith('/quote/') and path.endswith('/send') and method == 'POST':
        quote_id = int(path.split('/')[2])
        quote = update_quote_status(quote_id, 'sent')
        if quote:
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps(quote).encode()]
        else:
            start_response('404 Not Found', [('Content-Type', 'application/json')])
            return [json.dumps({'error': 'Quote not found'}).encode()]
    elif path == '/quotes' and method == 'GET':
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [json.dumps(load_quotes()).encode()]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']


def run_server(host='0.0.0.0', port=8000):
    with make_server(host, port, application) as httpd:
        print(f"Serving on {host}:{port}...")
        httpd.serve_forever()


if __name__ == '__main__':
    run_server()
