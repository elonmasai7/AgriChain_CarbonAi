document.addEventListener('DOMContentLoaded', () => {
  auth.init();

  const mobileToggle = document.querySelector('.mobile-toggle');
  const sidebar = document.querySelector('.sidebar');

  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });

    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 768) {
        if (!sidebar.contains(e.target) && !mobileToggle.contains(e.target)) {
          sidebar.classList.remove('open');
        }
      }
    });
  }

  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      auth.logout();
    });
  }

  const user = auth.user;
  if (user) {
    const nameEls = document.querySelectorAll('.user-name');
    nameEls.forEach(el => { el.textContent = user.full_name; });
    const roleEls = document.querySelectorAll('.user-role');
    roleEls.forEach(el => {
      const labels = { farmer: 'Farmer', buyer: 'Buyer', auditor: 'Auditor', admin: 'Administrator' };
      el.textContent = labels[user.role] || user.role;
    });
    const avatarEls = document.querySelectorAll('.user-avatar');
    avatarEls.forEach(el => {
      el.textContent = user.full_name.charAt(0).toUpperCase();
    });
  }

  if (window.location.pathname.includes('farmer-dashboard')) {
    farmerDashboard.init();
  } else if (window.location.pathname.includes('marketplace')) {
    marketplacePage.init();
  } else if (window.location.pathname.includes('carbon')) {
    carbonPage.init();
  } else if (window.location.pathname.includes('advisor')) {
    advisorPage.init();
  }
});
