const API = 'https://your-backend-service.onrender.com';

document.getElementById('searchForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const title = document.getElementById('title').value;
  const author = document.getElementById('author').value;
  const available = document.getElementById('available').value;

  const params = new URLSearchParams({ title, author, available });
  const res = await fetch(`${API}/books?${params}`);
  const books = await res.json();
  renderBooks(books);
});

function renderBooks(books) {
  const list = document.getElementById('bookList');
  list.innerHTML = '';
  books.forEach(book => {
    list.innerHTML += `
      <div class="book-card">
        <h3>${book.title}</h3>
        <p><strong>Author:</strong> ${book.author}</p>
        <p>${book.description}</p>
        <p><strong>₹${book.price}</strong></p>
        <p style="color: ${book.available ? 'green' : 'red'}">
          ${book.available ? 'In Stock' : 'Out of Stock'}
        </p>
      </div>
    `;
  });
}
