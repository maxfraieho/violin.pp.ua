// ОНОВЛЕНИЙ КОД ДЛЯ assets/js/main.js
// Замініть код форми на цей

document.addEventListener('DOMContentLoaded', function () {
  // Language switcher (залишається без змін)
  const frBtn = document.getElementById('fr-btn');
  const ukBtn = document.getElementById('uk-btn');
  const frBio = document.getElementById('fr-bio');
  const ukBio = document.getElementById('uk-bio');
  let currentLanguage = 'fr';

  if (frBtn && ukBtn && frBio && ukBio) {
    frBtn.addEventListener('click', () => {
      frBio.style.display = 'block';
      ukBio.style.display = 'none';
      currentLanguage = 'fr';
    });

    ukBtn.addEventListener('click', () => {
      ukBio.style.display = 'block';
      frBio.style.display = 'none';
      currentLanguage = 'uk';
    });
  }

  // Smooth scrolling (залишається без змін)
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

  // ==== НОВИЙ КОД: Telegram Integration ====
  
  const TELEGRAM_USERNAME = 'Kewobe'; // Username Telegram Арсена
  const WEBHOOK_URL = 'https://violin-telegram-webhook.maxfraieho.workers.dev'; // Cloudflare Worker URL

  // Швидкі повідомлення для Telegram
  const quickMessages = {
    'concert': {
      fr: 'Bonjour Arsen! Je voudrais réserver un concert. Pouvons-nous discuter des détails?',
      uk: 'Доброго дня, Арсене! Хотів би замовити концерт. Чи можемо обговорити деталі?'
    },
    'mariage': {
      fr: 'Bonjour Arsen! Je m\'intéresse à votre service pour un événement privé. Êtes-vous disponible?',
      uk: 'Доброго дня, Арсене! Цікавлюсь вашими послугами для приватної події. Чи ви вільні?'
    },
    'cours': {
      fr: 'Bonjour Arsen! Je voudrais prendre des cours de violon. Quels sont vos tarifs?',
      uk: 'Доброго дня, Арсене! Хотів би брати уроки скрипки. Які ваші ціни?'
    },
    'studio': {
      fr: 'Bonjour Arsen! Je recherche un violoniste pour un enregistrement. Pouvons-nous en parler?',
      uk: 'Доброго дня, Арсене! Шукаю скрипаля для студійного запису. Чи можемо поговорити?'
    }
  };

  // Обробка кнопок "Demander un Devis" / "Замовити"
  document.querySelectorAll('.service-cards a').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const href = this.getAttribute('href');
      const serviceMatch = href.match(/service=(\w+)/);
      
      if (serviceMatch) {
        const service = serviceMatch[1];
        const lang = currentLanguage;
        const message = quickMessages[service]?.[lang] || quickMessages['concert'][lang];
        
        // Питання: Telegram чи форма?
        const choice = confirm(
          lang === 'fr' 
            ? '📱 Ouvrir Telegram pour un contact rapide?\n\nOK = Telegram direct\nAnnuler = Formulaire détaillé'
            : '📱 Відкрити Telegram для швидкого зв\'язку?\n\nOK = Прямий Telegram\nСкасувати = Детальна форма'
        );
        
        if (choice) {
          // Відкрити Telegram
          const encodedMsg = encodeURIComponent(message);
          window.open(`https://t.me/${TELEGRAM_USERNAME}?text=${encodedMsg}`, '_blank');
        } else {
          // Прокрутити до форми
          document.querySelector('#contact').scrollIntoView({ behavior: 'smooth' });
          // Встановити тип сервісу
          setTimeout(() => {
            const serviceSelect = document.getElementById('service-type');
            const serviceMapping = {
              'concert': 'concert',
              'mariage': 'evenement-prive',
              'cours': 'enseignement',
              'studio': 'enregistrement'
            };
            if (serviceSelect && serviceMapping[service]) {
              serviceSelect.value = serviceMapping[service];
            }
          }, 500);
        }
      }
    });
  });

  // ==== Booking Form Wizard ====
  
  const progressBar = document.querySelector('.progress-bar');
  const steps = document.querySelectorAll('.form-step');
  let currentStep = 1;

  function showStep(step) {
    steps.forEach((s) => (s.style.display = 'none'));
    const stepElement = document.getElementById(`step-${step}`);
    if (stepElement) {
      stepElement.style.display = 'block';
    }
    const progress = (step / steps.length) * 100;
    if (progressBar) {
      progressBar.style.width = `${progress}%`;
      progressBar.setAttribute('aria-valuenow', progress);
    }
  }

  // Navigation між кроками
  const nextBtn1 = document.getElementById('next-1');
  const prevBtn2 = document.getElementById('prev-2');
  const nextBtn2 = document.getElementById('next-2');
  const prevBtn3 = document.getElementById('prev-3');
  const nextBtn3 = document.getElementById('next-3');
  const prevBtn4 = document.getElementById('prev-4');
  const submitBtn = document.getElementById('submit-form');

  if (nextBtn1) nextBtn1.addEventListener('click', () => { currentStep = 2; showStep(currentStep); });
  if (prevBtn2) prevBtn2.addEventListener('click', () => { currentStep = 1; showStep(currentStep); });
  if (nextBtn2) nextBtn2.addEventListener('click', () => { currentStep = 3; showStep(currentStep); });
  if (prevBtn3) prevBtn3.addEventListener('click', () => { currentStep = 2; showStep(currentStep); });
  if (nextBtn3) nextBtn3.addEventListener('click', () => { currentStep = 4; showStep(currentStep); });
  if (prevBtn4) prevBtn4.addEventListener('click', () => { currentStep = 3; showStep(currentStep); });

  // Відправка форми в Telegram
  if (submitBtn) {
    submitBtn.addEventListener('click', async () => {
      const formData = {
        serviceType: document.getElementById('service-type').value,
        eventDate: document.getElementById('event-date').value,
        eventLocation: document.getElementById('event-location').value,
        repertoireDetails: document.getElementById('repertoire-details').value,
        contactName: document.getElementById('contact-name').value,
        contactEmail: document.getElementById('contact-email').value,
        phone: document.getElementById('contact-phone')?.value || '',
        language: currentLanguage
      };

      // Валідація
      if (!formData.serviceType || formData.serviceType === 'Choisir...') {
        alert(currentLanguage === 'fr' ? 'Veuillez choisir un service' : 'Оберіть послугу');
        return;
      }
      if (!formData.contactName || !formData.contactEmail) {
        alert(currentLanguage === 'fr' ? 'Veuillez remplir votre nom et email' : 'Заповніть ім\'я та email');
        return;
      }

      // Показати індикатор завантаження
      submitBtn.disabled = true;
      submitBtn.textContent = currentLanguage === 'fr' ? 'Envoi...' : 'Відправка...';

      try {
        // Відправка на Cloudflare Worker
        const response = await fetch(WEBHOOK_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.success) {
          alert(currentLanguage === 'fr' 
            ? '✅ Votre demande a été envoyée avec succès! Arsen vous contactera bientôt.' 
            : '✅ Ваш запит успішно відправлено! Арсен зв\'яжеться з вами найближчим часом.');
          
          // Скинути форму
          document.querySelectorAll('.form-step input, .form-step textarea, .form-step select').forEach(el => {
            if (el.tagName === 'SELECT') el.selectedIndex = 0;
            else el.value = '';
          });
          currentStep = 1;
          showStep(currentStep);
        } else {
          throw new Error(result.error || 'Unknown error');
        }
      } catch (error) {
        console.error('Error:', error);
        alert(currentLanguage === 'fr'
          ? '❌ Erreur lors de l\'envoi. Veuillez réessayer ou contactez directement via Telegram.'
          : '❌ Помилка відправки. Спробуйте знову або зв\'яжіться напряму через Telegram.');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = currentLanguage === 'fr' ? 'Envoyer' : 'Відправити';
      }
    });
  }

  showStep(currentStep);
});