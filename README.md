# Scopeio Prototype

This repository contains a minimal prototype for a quoting tool.

## Features
- **Pricing Library** stored in `pricing.json`
- **Quote Management** via HTTP endpoints
  - `GET /pricing` – list pricing items
  - `POST /quote` – create a quote with JSON payload `{ "customer": "name", "items": [...] }`
  - `GET /quote/<id>` – retrieve a quote
  - `POST /quote/<id>/send` – mark a quote as sent
  - `GET /quotes` – list all quotes

Quotes are stored in `quotes.json` and their status is tracked (draft/sent).

## Running
```
python server.py
```

## Testing
```
python -m unittest discover -s tests
```
