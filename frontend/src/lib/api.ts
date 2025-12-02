import axios, { AxiosInstance } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request Interceptor: Add JWT Token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response Interceptor: Handle 401 (Token Expired)
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.clearToken();
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // ============== Token Management ==============

  getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }

  setToken(token: string) {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
  }

  clearToken() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    }
  }

  // ============== Auth Endpoints ==============

  async register(email: string, name: string, password: string) {
    const { data } = await this.client.post('/api/auth/register', {
      email,
      name,
      password,
    });
    this.setToken(data.tokens.access_token);
    localStorage.setItem('refresh_token', data.tokens.refresh_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  }

  async login(email: string, password: string) {
    const { data } = await this.client.post('/api/auth/login', {
      email,
      password,
    });
    this.setToken(data.tokens.access_token);
    localStorage.setItem('refresh_token', data.tokens.refresh_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  }

  async getCurrentUser() {
    const { data } = await this.client.get('/api/auth/me');
    return data;
  }

  logout() {
    this.clearToken();
  }

  // ============== Content Endpoints ==============

  async generateHook(prompt: string, context?: string) {
    const { data } = await this.client.post('/api/content/hook', {
      prompt,
      context,
    });
    return data;
  }

  async generateScript(prompt: string, context?: string, duration_seconds = 15) {
    const { data } = await this.client.post('/api/content/script', {
      prompt,
      context,
      duration_seconds,
    });
    return data;
  }

  async generateShotlist(prompt: string, context?: string, script?: string) {
    const { data } = await this.client.post('/api/content/shotlist', {
      prompt,
      context,
      script,
    });
    return data;
  }

  async generateVoiceover(prompt: string, context?: string, script?: string) {
    const { data } = await this.client.post('/api/content/voiceover', {
      prompt,
      context,
      script,
    });
    return data;
  }

  async generateCaption(prompt: string, context?: string, include_emojis = true) {
    const { data } = await this.client.post('/api/content/caption', {
      prompt,
      context,
      include_emojis,
    });
    return data;
  }

  async generateBRoll(prompt: string, context?: string) {
    const { data } = await this.client.post('/api/content/broll', {
      prompt,
      context,
    });
    return data;
  }

  async generateCalendar(niche: string, prompt: string, context?: string) {
    const { data } = await this.client.post('/api/content/calendar', {
      niche,
      prompt,
      context,
    });
    return data;
  }

  // ============== Subscription Endpoints ==============

  async createCheckoutSession(plan: string, success_url: string, cancel_url: string) {
    const { data } = await this.client.post('/api/subscription/checkout', {
      plan,
      success_url,
      cancel_url,
    });
    return data;
  }

  async createPortalSession(return_url: string) {
    const { data } = await this.client.post('/api/subscription/portal', {
      return_url,
    });
    return data;
  }

  async getSubscriptionStatus() {
    const { data } = await this.client.get('/api/subscription/status');
    return data;
  }

  // ============== Export Endpoints ==============

  async exportPDF(content_id: string) {
    const response = await this.client.get(`/api/export/pdf/${content_id}`, {
      responseType: 'blob',
    });
    return response.data;
  }
}

export const api = new ApiClient();
