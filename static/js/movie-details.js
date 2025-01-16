document.addEventListener('DOMContentLoaded', function() {
    // Favorite Toggle
    const favoriteBtn = document.getElementById('favoriteBtn');
    if (favoriteBtn) {
        favoriteBtn.addEventListener('click', function() {
            const movieSlug = this.dataset.movie;
            fetch(`/movies/${movieSlug}/favorite/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_favorite) {
                    this.classList.add('active');
                } else {
                    this.classList.remove('active');
                }
            });
        });
    }

    // Watchlist Toggle
    const watchlistBtn = document.getElementById('watchlistBtn');
    if (watchlistBtn) {
        watchlistBtn.addEventListener('click', function() {
            const movieSlug = this.dataset.movie;
            fetch(`/movies/${movieSlug}/watchlist/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.in_watch_list) {
                    this.classList.add('active');
                } else {
                    this.classList.remove('active');
                }
            });
        });
    }
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 