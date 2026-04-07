/* ============================================
   Redwood Real Estate Solutions — App Logic
   Dark mode, FAQ, form, mobile menu, scroll
   ============================================ */

(function () {
  'use strict';

  // ---- Dark Mode Toggle ----
  const toggle = document.querySelector('[data-theme-toggle]');
  const root = document.documentElement;
  let theme = 'dark';
  root.setAttribute('data-theme', theme);
  updateToggleIcon();

  if (toggle) {
    toggle.addEventListener('click', function () {
      theme = theme === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', theme);
      toggle.setAttribute('aria-label', 'Switch to ' + (theme === 'dark' ? 'light' : 'dark') + ' mode');
      updateToggleIcon();
    });
  }

  function updateToggleIcon() {
    if (!toggle) return;
    toggle.innerHTML = theme === 'dark'
      ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
      : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  }

  // ---- Hero Image Slideshow ----
  var slides = document.querySelectorAll('.hero__slide');
  var dots = document.querySelectorAll('.hero__progress-dot');
  var currentSlide = 0;
  var slideInterval = null;
  var SLIDE_DURATION = 5000; // 5 seconds per slide

  function goToSlide(index) {
    slides.forEach(function (s) { s.classList.remove('is-active'); });
    dots.forEach(function (d) { d.classList.remove('is-active'); });
    currentSlide = index;
    if (slides[currentSlide]) slides[currentSlide].classList.add('is-active');
    if (dots[currentSlide]) dots[currentSlide].classList.add('is-active');
  }

  function nextSlide() {
    goToSlide((currentSlide + 1) % slides.length);
  }

  function startSlideshow() {
    if (slideInterval) clearInterval(slideInterval);
    slideInterval = setInterval(nextSlide, SLIDE_DURATION);
  }

  if (slides.length > 1) {
    startSlideshow();
    dots.forEach(function (dot) {
      dot.addEventListener('click', function () {
        var idx = parseInt(this.getAttribute('data-slide'), 10);
        goToSlide(idx);
        startSlideshow(); // Reset timer
      });
    });
  }

  // ---- Header Scroll State ----
  var header = document.querySelector('.header');
  if (header) {
    var lastScroll = 0;
    window.addEventListener('scroll', function () {
      var scroll = window.scrollY;
      if (scroll > 50) {
        header.classList.add('header--scrolled');
      } else {
        header.classList.remove('header--scrolled');
      }
      lastScroll = scroll;
    }, { passive: true });
  }

  // ---- Mobile Menu ----
  var mobileMenu = document.getElementById('mobile-menu');
  var openBtn = document.querySelector('[data-mobile-open]');
  var closeBtn = document.querySelector('[data-mobile-close]');
  var mobileLinks = document.querySelectorAll('[data-mobile-link]');

  function openMenu() {
    if (mobileMenu) {
      mobileMenu.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    }
  }
  function closeMenu() {
    if (mobileMenu) {
      mobileMenu.classList.remove('is-open');
      document.body.style.overflow = '';
    }
  }

  if (openBtn) openBtn.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  mobileLinks.forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });

  // ---- FAQ Accordion ----
  var faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(function (item) {
    var trigger = item.querySelector('.faq-item__trigger');
    if (trigger) {
      trigger.addEventListener('click', function () {
        var isOpen = item.classList.contains('is-open');

        // Close all other items
        faqItems.forEach(function (other) {
          other.classList.remove('is-open');
          var otherTrigger = other.querySelector('.faq-item__trigger');
          if (otherTrigger) otherTrigger.setAttribute('aria-expanded', 'false');
        });

        // Toggle current
        if (!isOpen) {
          item.classList.add('is-open');
          trigger.setAttribute('aria-expanded', 'true');
        }
      });
    }
  });

  // ---- Lead Form Submission ----
  // Sends data to Go High Level via webhook
  // Handles both hero form and bottom CTA form
  var GHL_WEBHOOK_URL = 'YOUR_GHL_WEBHOOK_URL';

  function handleFormSubmit(formEl, successEl) {
    if (!formEl) return;
    formEl.addEventListener('submit', function (e) {
      e.preventDefault();

      var inputs = formEl.querySelectorAll('input[required]');
      var isValid = true;

      inputs.forEach(function (input) {
        if (!input.value.trim()) {
          input.style.borderColor = 'var(--color-primary)';
          isValid = false;
        } else {
          input.style.borderColor = '';
        }
      });

      if (!isValid) return;

      // Prepare form data for Go High Level webhook
      var formData = new FormData();
      formData.append('full_name', formEl.querySelector('[name="full_name"]').value.trim());
      formData.append('property_address', formEl.querySelector('[name="property_address"]').value.trim());
      formData.append('email', formEl.querySelector('[name="email"]').value.trim());
      formData.append('phone', formEl.querySelector('[name="phone"]').value.trim());
      formData.append('source', 'Redwood Real Estate Website');

      // Send to Go High Level webhook
      // Replace YOUR_GHL_WEBHOOK_URL with your actual Go High Level inbound webhook URL
      if (GHL_WEBHOOK_URL !== 'YOUR_GHL_WEBHOOK_URL') {
        fetch(GHL_WEBHOOK_URL, {
          method: 'POST',
          body: formData,
        }).catch(function (err) {
          console.log('Webhook delivery attempted:', err);
        });
      }

      // Show success state
      formEl.style.display = 'none';
      if (successEl) successEl.classList.add('is-visible');

      // Track conversion event for Google/Meta ads
      if (typeof gtag === 'function') {
        gtag('event', 'generate_lead', {
          event_category: 'form',
          event_label: 'cash_offer_request'
        });
      }
      if (typeof fbq === 'function') {
        fbq('track', 'Lead', {
          content_name: 'Cash Offer Request',
          content_category: 'Real Estate'
        });
      }
    });
  }

  // Hero form
  handleFormSubmit(
    document.getElementById('offer-form-hero'),
    document.getElementById('form-success-hero')
  );
  // Bottom CTA form
  handleFormSubmit(
    document.getElementById('offer-form'),
    document.getElementById('form-success')
  );

  // ---- Smooth Scroll for Anchor Links ----
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });



})();
