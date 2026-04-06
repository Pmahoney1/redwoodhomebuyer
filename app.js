/* ============================================
   Redwood Real Estate Solutions — App Logic
   Dark mode, FAQ, form, mobile menu, scroll
   ============================================ */

(function () {
  'use strict';

  // ---- Dark Mode Toggle ----
  const toggle = document.querySelector('[data-theme-toggle]');
  const root = document.documentElement;
  let theme = matchMedia('(prefers-color-scheme:dark)').matches ? 'dark' : 'light';
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
  var form = document.getElementById('offer-form');
  var formSuccess = document.getElementById('form-success');

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Basic validation
      var name = document.getElementById('full-name');
      var address = document.getElementById('property-address');
      var email = document.getElementById('email');
      var phone = document.getElementById('phone');
      var isValid = true;

      [name, address, email, phone].forEach(function (input) {
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
      formData.append('full_name', name.value.trim());
      formData.append('property_address', address.value.trim());
      formData.append('email', email.value.trim());
      formData.append('phone', phone.value.trim());
      formData.append('source', 'Redwood Real Estate Website');

      // Send to Go High Level webhook
      // Replace YOUR_GHL_WEBHOOK_URL with your actual Go High Level inbound webhook URL
      // To find this: Go High Level → Automation → Workflows → Create Workflow → 
      // Add Trigger → Inbound Webhook → Copy the webhook URL
      var GHL_WEBHOOK_URL = 'YOUR_GHL_WEBHOOK_URL';

      if (GHL_WEBHOOK_URL !== 'YOUR_GHL_WEBHOOK_URL') {
        fetch(GHL_WEBHOOK_URL, {
          method: 'POST',
          body: formData,
        }).catch(function (err) {
          console.log('Webhook delivery attempted:', err);
        });
      }

      // Show success state regardless (better UX)
      form.style.display = 'none';
      if (formSuccess) formSuccess.classList.add('is-visible');

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

  // ---- Animate Trust Numbers on Scroll ----
  function animateValue(el, end, duration) {
    var start = 0;
    var startTime = null;
    var numericEnd = parseInt(end.replace(/[^0-9]/g, ''), 10);
    var suffix = end.replace(/[0-9]/g, '');
    var prefix = end.match(/^\D+/) ? end.match(/^\D+/)[0] : '';

    if (isNaN(numericEnd)) {
      el.textContent = end;
      return;
    }

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var current = Math.round(eased * numericEnd);
      el.textContent = prefix + current + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  var trustValues = document.querySelectorAll('.hero__trust-value');
  var hasAnimated = false;

  function checkTrustVisible() {
    if (hasAnimated) return;
    var trustSection = document.querySelector('.hero__trust');
    if (!trustSection) return;
    var rect = trustSection.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      hasAnimated = true;
      trustValues.forEach(function (el) {
        if (el.hasAttribute('data-no-animate')) return;
        var text = el.textContent;
        animateValue(el, text, 800);
      });
    }
  }

  window.addEventListener('scroll', checkTrustVisible, { passive: true });
  // Run once on load
  setTimeout(checkTrustVisible, 200);

})();
