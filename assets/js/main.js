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
      // Security: validate href is anchor link
      if (targetId && targetId.startsWith('#')) {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          targetElement.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });

  // Booking Form Wizard
  const progressBar = document.querySelector('.progress-bar');
  const steps = document.querySelectorAll('.form-step');
  let currentStep = 1;

  function showStep(step) {
    if (!progressBar || steps.length === 0) return;
    steps.forEach((s) => (s.style.display = 'none'));
    const stepElement = document.getElementById(`step-${step}`);
    if (stepElement) {
      stepElement.style.display = 'block';
    }
    const progress = (step / steps.length) * 100;
    progressBar.style.width = `${progress}%`;
    progressBar.setAttribute('aria-valuenow', progress);
  }

  // Add event listeners with null checks
  const wizardButtons = [
    { id: 'next-1', action: () => { currentStep = 2; showStep(currentStep); } },
    { id: 'prev-2', action: () => { currentStep = 1; showStep(currentStep); } },
    { id: 'next-2', action: () => { currentStep = 3; showStep(currentStep); } },
    { id: 'prev-3', action: () => { currentStep = 2; showStep(currentStep); } },
    { id: 'next-3', action: () => { currentStep = 4; showStep(currentStep); } },
    { id: 'prev-4', action: () => { currentStep = 3; showStep(currentStep); } }
  ];

  wizardButtons.forEach(({ id, action }) => {
    const button = document.getElementById(id);
    if (button) {
      button.addEventListener('click', action);
    }
  });

  const submitButton = document.getElementById('submit-form');
  if (submitButton) {
    submitButton.addEventListener('click', () => {
      // Validate form data
      const formElements = {
        serviceType: document.getElementById('service-type'),
        eventDate: document.getElementById('event-date'),
        eventLocation: document.getElementById('event-location'),
        repertoireDetails: document.getElementById('repertoire-details'),
        contactName: document.getElementById('contact-name'),
        contactEmail: document.getElementById('contact-email')
      };

      // Check if all elements exist
      if (!Object.values(formElements).every(el => el)) {
        console.error('Form elements missing');
        return;
      }

      const formData = {
        serviceType: formElements.serviceType.value,
        eventDate: formElements.eventDate.value,
        eventLocation: formElements.eventLocation.value,
        repertoireDetails: formElements.repertoireDetails.value,
        contactName: formElements.contactName.value,
        contactEmail: formElements.contactEmail.value
      };

      // Basic validation
      if (!formData.contactEmail || !formData.contactName) {
        alert('Veuillez remplir tous les champs obligatoires.');
        return;
      }

      // TODO: Replace with actual webhook endpoint
      // For development only - remove in production
      if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log('Form data (dev only):', formData);
      }

      // Show success message (consider using Bootstrap toast instead)
      alert('Votre demande a été envoyée !');

      // Reset form
      currentStep = 1;
      showStep(currentStep);
      const bookingForm = document.getElementById('booking-form');
      if (bookingForm) {
        bookingForm.reset();
      }
    });
  }

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
