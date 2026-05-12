const auth = {
  init() {
    api.loadTokens();
    const user = localStorage.getItem('user');
    if (user) {
      try { auth._user = JSON.parse(user); } catch { auth._user = null; }
    }
  },

  _user: null,

  get user() { return auth._user; },

  async login(username, password) {
    const data = await api.post('/auth/login', { username, password });
    api.setTokens(data.access_token, data.refresh_token);
    const profile = await api.get('/auth/me');
    auth._user = profile;
    localStorage.setItem('user', JSON.stringify(profile));
    return profile;
  },

  async register(data) {
    const user = await api.post('/auth/register', data);
    return user;
  },

  logout() {
    api.clearTokens();
    auth._user = null;
    window.location.href = '/';
  },

  isAuthenticated() {
    return !!api._token;
  },

  getRole() {
    return auth._user?.role || null;
  },

  requireAuth() {
    if (!auth.isAuthenticated()) {
      window.location.href = '/';
      return false;
    }
    return true;
  },
};
