function openModal(id) {
    document.getElementById(id).style.display = "block";
}

function closeModal(id) {
    document.getElementById(id).style.display = "none";
}

// Закриття при кліку поза модальним вікном
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
}

setTimeout(function () {
    const toast = document.getElementById('toast-message');
    if (toast) toast.remove();
}, 4000); // зникне через 4 секунди


document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('search-input');
  const suggestions = document.getElementById('suggestions');
  const searchBar = document.querySelector('.search-bar');
  const form = searchBar.querySelector('form');

  let latestResults = []; // Зберігаємо останні знайдені результати

  input.addEventListener('input', function() {
    const query = this.value;

    if (query.length < 2) {
      suggestions.innerHTML = '';
      searchBar.classList.remove('has-suggestions');
      latestResults = [];
      return;
    }

    fetch(`/search/?q=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        suggestions.innerHTML = '';
        latestResults = data.results || [];

        if (latestResults.length > 0) {
          searchBar.classList.add('has-suggestions');
        } else {
          searchBar.classList.remove('has-suggestions');
        }

        latestResults.forEach(item => {
          const li = document.createElement('li');
          li.innerHTML = `<a href="/work/${item.link}/">${item.title}</a>`;
          suggestions.appendChild(li);
        });
      });
  });

  // ⏩ Обробка submit — переходимо на перший результат
  form.addEventListener('submit', function(e) {
      if (latestResults.length === 0) {
        e.preventDefault(); // Забороняємо відправку форми, якщо нема результатів
        return;
      }

      e.preventDefault(); // Забороняємо стандартну дію
      const firstResult = latestResults[0];
      window.location.href = `/work/${firstResult.link}/`; // Переходимо до першого результату
    });

  // Ховати підказки при кліку поза
  document.addEventListener('click', function(e) {
    if (!input.contains(e.target) && !suggestions.contains(e.target)) {
      suggestions.innerHTML = '';
      searchBar.classList.remove('has-suggestions');
    }
  });
});

