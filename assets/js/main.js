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

  // Booking Form Wizard
  const progressBar = document.querySelector('.progress-bar');
  const steps = document.querySelectorAll('.form-step');
  let currentStep = 1;

  function showStep(step) {
    steps.forEach((s) => (s.style.display = 'none'));
    document.getElementById(`step-${step}`).style.display = 'block';
    const progress = (step / steps.length) * 100;
    progressBar.style.width = `${progress}%`;
    progressBar.setAttribute('aria-valuenow', progress);
  }

  document.getElementById('next-1').addEventListener('click', () => {
    currentStep = 2;
    showStep(currentStep);
  });
  document.getElementById('prev-2').addEventListener('click', () => {
    currentStep = 1;
    showStep(currentStep);
  });
  document.getElementById('next-2').addEventListener('click', () => {
    currentStep = 3;
    showStep(currentStep);
  });
  document.getElementById('prev-3').addEventListener('click', () => {
    currentStep = 2;
    showStep(currentStep);
  });
  document.getElementById('next-3').addEventListener('click', () => {
    currentStep = 4;
    showStep(currentStep);
  });
  document.getElementById('prev-4').addEventListener('click', () => {
    currentStep = 3;
    showStep(currentStep);
  });

  document.getElementById('submit-form').addEventListener('click', () => {
    const formData = {
      serviceType: document.getElementById('service-type').value,
      eventDate: document.getElementById('event-date').value,
      eventLocation: document.getElementById('event-location').value,
      repertoireDetails: document.getElementById('repertoire-details').value,
      contactName: document.getElementById('contact-name').value,
      contactEmail: document.getElementById('contact-email').value,
    };

    // Replace with actual webhook endpoint
    console.log('Form data:', formData);
    alert('Votre demande a été envoyée !');

    // Reset form
    currentStep = 1;
    showStep(currentStep);
    document.getElementById('booking-form').reset();
  });

  showStep(currentStep);

  // Gallery Filter
  const filterButtons = document.querySelectorAll('.filter-btn');
  const galleryItems = document.querySelectorAll('.gallery-item');

  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Set active class
      filterButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');

      const filter = button.getAttribute('data-filter');

      galleryItems.forEach(item => {
        if (filter === 'all' || item.getAttribute('data-category') === filter) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });

  // Wavesurfer Audio Player
  if (document.getElementById('waveform-container')) {
    const wavesurfer = WaveSurfer.create({
      container: '#waveform-container',
      waveColor: '#adb5bd',
      progressColor: '#343a40',
      barWidth: 2,
      height: 100,
      responsive: true
    });

    // Uncomment and replace with a real audio file path when available
    // wavesurfer.load('path/to/your/audio.mp3');

    const playPauseBtn = document.getElementById('play-pause-btn');
    playPauseBtn.addEventListener('click', () => {
      wavesurfer.playPause();
    });
  }
});
