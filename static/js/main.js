// Burger menu
document.getElementById('burger')?.addEventListener('click', () => {
  document.getElementById('mobileNav')?.classList.toggle('open');
});

// Auto-dismiss alerts
setTimeout(() => {
  document.querySelectorAll('.alert').forEach(el => {
    el.style.transition = 'opacity .5s';
    el.style.opacity = '0';
  });
}, 4000);

// Thumbnail gallery
document.querySelectorAll('.thumb-strip img').forEach(thumb => {
  thumb.addEventListener('click', function() {
    document.querySelector('.main-photo img').src = this.src;
    document.querySelectorAll('.thumb-strip img').forEach(t => t.classList.remove('active'));
    this.classList.add('active');
  });
});

// AJAX Favorite toggle
document.querySelectorAll('.fav-btn, .btn-fav-detail').forEach(btn => {
  btn.addEventListener('click', function(e) {
    e.preventDefault();
    const carId = this.dataset.carId;
    if (!carId) return;
    fetch(`/cars/car/${carId}/favorite/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'X-Requested-With': 'XMLHttpRequest'
      },
    })
    .then(r => r.json())
    .then(data => {
      const isDetail = this.classList.contains('btn-fav-detail');
      if (data.status === 'added') {
        this.textContent = isDetail ? '❤️ В избранном' : '❤️';
      } else {
        this.textContent = isDetail ? '🤍 В избранное' : '🤍';
      }
    });
  });
});

// Dynamic model loading by brand
const brandSelect = document.getElementById('id_brand');
const modelSelect = document.getElementById('id_model');
if (brandSelect && modelSelect) {
  brandSelect.addEventListener('change', function() {
    const brandId = this.value;
    if (!brandId) {
      modelSelect.innerHTML = '<option value="">-- Выберите модель --</option>';
      return;
    }
    fetch(`/cars/api/models/?brand_id=${brandId}`)
      .then(r => r.json())
      .then(data => {
        modelSelect.innerHTML = '<option value="">-- Выберите модель --</option>';
        data.models.forEach(m => {
          const opt = document.createElement('option');
          opt.value = m.id;
          opt.textContent = m.name;
          modelSelect.appendChild(opt);
        });
      });
  });
}

function getCookie(name) {
  let value = `; ${document.cookie}`;
  let parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}