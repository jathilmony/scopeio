import os
import server
import unittest

class QuoteTests(unittest.TestCase):
    def setUp(self):
        if os.path.exists(server.QUOTES_FILE):
            os.remove(server.QUOTES_FILE)

    def test_create_quote(self):
        data = {'customer': 'John Doe', 'items': [{'id': 1, 'quantity': 2}]}
        quote = server.create_quote(data)
        self.assertEqual(quote['id'], 1)
        self.assertEqual(quote['status'], 'draft')
        quotes = server.load_quotes()
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0]['customer'], 'John Doe')

    def test_update_quote_status(self):
        data = {'customer': 'Jane', 'items': []}
        quote = server.create_quote(data)
        updated = server.update_quote_status(quote['id'], 'sent')
        self.assertEqual(updated['status'], 'sent')
        quotes = server.load_quotes()
        self.assertEqual(quotes[0]['status'], 'sent')

if __name__ == '__main__':
    unittest.main()
