document.addEventListener('DOMContentLoaded', function () {
  // Language switcher
  const frBtn = document.getElementById('fr-btn');
  const ukBtn = document.getElementById('uk-btn');
  const frBio = document.getElementById('fr-bio');
  const ukBio = document.getElementById('uk-bio');

  if (frBtn && ukBtn && frBio && ukBio) {
    frBtn.addEventListener('click', () => {
      frBio.style.display = 'block';
      ukBio.style.display = 'none';
    });

    ukBtn.addEventListener('click', () => {
      ukBio.style.display = 'block';
      frBio.style.display = 'none';
    });
  }

  // Gallery Modal
  const galleryModal = document.getElementById('galleryModal');
  if (galleryModal) {
    galleryModal.addEventListener('show.bs.modal', function (event) {
      const button = event.relatedTarget;
      const imageUrl = button.getAttribute('href');
      const modalImage = galleryModal.querySelector('#modalImage');
      modalImage.setAttribute('src', imageUrl);
    });
  }

  // Smooth scrolling
  const navLinks = document.querySelectorAll('.navigation');
  navLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});
