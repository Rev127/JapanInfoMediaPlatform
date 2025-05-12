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
