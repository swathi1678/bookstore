const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const Book = require('./models/Book');

app.get('/books', async (req, res) => {
  const { title, author, available } = req.query;
  const filter = {};
  if (title) filter.title = new RegExp(title, 'i');
  if (author) filter.author = new RegExp(author, 'i');
  if (available) filter.available = available === 'true';
  const books = await Book.find(filter);
  res.json(books);
});

app.post('/books', async (req, res) => {
  const book = new Book(req.body);
  await book.save();
  res.json({ status: 'Book saved' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
