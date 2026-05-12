const API_BASE = 'http://localhost:8000/api';

const api = {
  _token: null,
  _refreshToken: null,

  setTokens(access, refresh) {
    this._token = access;
    this._refreshToken = refresh;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  },

  loadTokens() {
    this._token = localStorage.getItem('access_token');
    this._refreshToken = localStorage.getItem('refresh_token');
  },

  clearTokens() {
    this._token = null;
    this._refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  getHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    if (this._token) {
      headers['Authorization'] = `Bearer ${this._token}`;
    }
    return headers;
  },

  async request(method, path, body = null) {
    const url = `${API_BASE}${path}`;
    const options = { method, headers: this.getHeaders() };
    if (body) options.body = JSON.stringify(body);

    try {
      const res = await fetch(url, options);
      if (res.status === 401 && this._refreshToken) {
        const refreshed = await this.refresh();
        if (refreshed) {
          options.headers = this.getHeaders();
          const retry = await fetch(url, options);
          return retry.json();
        }
      }
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      return res.json();
    } catch (err) {
      throw err;
    }
  },

  async refresh() {
    try {
      const res = await fetch(`${API_BASE}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: this._refreshToken }),
      });
      if (!res.ok) {
        this.clearTokens();
        window.location.href = '/';
        return false;
      }
      const data = await res.json();
      this.setTokens(data.access_token, data.refresh_token);
      return true;
    } catch {
      this.clearTokens();
      window.location.href = '/';
      return false;
    }
  },

  get(path) { return this.request('GET', path); },
  post(path, body) { return this.request('POST', path, body); },
  patch(path, body) { return this.request('PATCH', path, body); },
  put(path, body) { return this.request('PUT', path, body); },
  del(path) { return this.request('DELETE', path); },
};
