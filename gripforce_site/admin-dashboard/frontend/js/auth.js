const API_BASE = window.location.origin;

// LOGIN
const loginForm = document.getElementById('login-form');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value.trim().toLowerCase();
    const password = document.getElementById('password').value;
    const errorEl = document.getElementById('login-error');

    try {
      const res = await fetch(`${API_BASE}/api/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      if (!res.ok) throw new Error('Invalid');
      const data = await res.json();
      localStorage.setItem('gripforce_admin_token', data.token);
      localStorage.setItem('gripforce_admin_user', JSON.stringify(data.user));
      window.location.href = '/app.html';
    } catch (err) {
      errorEl.classList.add('visible');
    }
  });
}

// CHECK AUTH
function getToken() {
  const t = localStorage.getItem('gripforce_admin_token');
  if (!t) { window.location.href = '/'; return null; }
  return t;
}

async function api(url, options = {}) {
  const token = getToken();
  if (!token) throw new Error('No token');
  const res = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers
    }
  });
  if (res.status === 401) {
    localStorage.clear();
    window.location.href = '/';
    throw new Error('Unauthorized');
  }
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Erreur' }));
    throw new Error(err.detail || 'Erreur');
  }
  return res.json();
}

// LOGOUT
function logout() {
  localStorage.clear();
  window.location.href = '/';
}

// USER INFO
function getUser() {
  try { return JSON.parse(localStorage.getItem('gripforce_admin_user')); }
  catch { return null; }
}
