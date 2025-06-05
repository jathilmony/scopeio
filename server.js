const express = require('express');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const PORT = 8000;

const PRICING_FILE = 'pricing.json';
const QUOTES_FILE = 'quotes.json';

app.use(express.json());

// Load pricing data
async function loadPricing() {
  try {
    const data = await fs.readFile(PRICING_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Error loading pricing:', error);
    return {};
  }
}

// Load quotes data
async function loadQuotes() {
  try {
    const data = await fs.readFile(QUOTES_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    if (error.code === 'ENOENT') {
      return [];
    }
    console.error('Error loading quotes:', error);
    return [];
  }
}

// Save quotes data
async function saveQuotes(quotes) {
  await fs.writeFile(QUOTES_FILE, JSON.stringify(quotes, null, 2));
}

// Get pricing
app.get('/pricing', async (req, res) => {
  const pricing = await loadPricing();
  res.json(pricing);
});

// Create quote
app.post('/quote', async (req, res) => {
  const quotes = await loadQuotes();
  const quoteId = quotes.length + 1;
  const quote = {
    id: quoteId,
    customer: req.body.customer || 'Unknown',
    items: req.body.items || [],
    status: 'draft'
  };
  quotes.push(quote);
  await saveQuotes(quotes);
  res.status(201).json(quote);
});

// Get specific quote
app.get('/quote/:id', async (req, res) => {
  const quoteId = parseInt(req.params.id);
  const quotes = await loadQuotes();
  const quote = quotes.find(q => q.id === quoteId);
  
  if (quote) {
    res.json(quote);
  } else {
    res.status(404).json({ error: 'Quote not found' });
  }
});

// Send quote
app.post('/quote/:id/send', async (req, res) => {
  const quoteId = parseInt(req.params.id);
  const quotes = await loadQuotes();
  const quote = quotes.find(q => q.id === quoteId);
  
  if (quote) {
    quote.status = 'sent';
    await saveQuotes(quotes);
    res.json(quote);
  } else {
    res.status(404).json({ error: 'Quote not found' });
  }
});

// Get all quotes
app.get('/quotes', async (req, res) => {
  const quotes = await loadQuotes();
  res.json(quotes);
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});