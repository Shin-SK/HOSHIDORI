document.addEventListener('DOMContentLoaded', function() {
    const starRating = document.getElementById('star-rating');
    if (!starRating) return   // ★ ← これだけでエラーは止まる
    const ratingInput = document.getElementById('rating-input');
    const stars = starRating.querySelectorAll('i.fas.fa-star');

    // 初期表示 (hidden inputの値を取得→塗りつぶし)
    highlightStars(ratingInput.value);

    // 各星をクリック
    stars.forEach(star => {
        star.addEventListener('click', () => {
            const selectedValue = star.getAttribute('data-value');
            ratingInput.value = selectedValue;
            highlightStars(selectedValue);
        });
    });

    function highlightStars(rating) {
        stars.forEach(star => {
            const starValue = parseInt(star.getAttribute('data-value'));
            if (starValue <= parseInt(rating)) {
                star.classList.add('selected');
            } else {
                star.classList.remove('selected');
            }
        });
    }
});