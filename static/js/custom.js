FilePond.registerPlugin(FilePondPluginImagePreview);

document.addEventListener('DOMContentLoaded', function() {
    // poster用
    const posterInput = document.querySelector('#poster-upload');
    if (posterInput) {
      FilePond.create(posterInput, {
          server: null,
          storeAsFile: true,
          labelIdle: '<span class="filepond--label-action"><i class="fas fa-plus"></i></span>',
          allowImagePreview: true,
          stylePanelAspectRatio: 'auto',
          imagePreviewMaxHeight: 9999,
      });
    }

    // icon用（同じ設定を使う）
    const iconInput = document.querySelector('#icon-upload');
    if (iconInput) {
      FilePond.create(iconInput, {
          server: null,
          storeAsFile: true,
          labelIdle: '<span class="filepond--label-action"><i class="fas fa-plus"></i></span>',
          allowImagePreview: true,
          stylePanelAspectRatio: 'auto',
          imagePreviewMaxHeight: 9999,
      });
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const starRating = document.getElementById('star-rating');
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