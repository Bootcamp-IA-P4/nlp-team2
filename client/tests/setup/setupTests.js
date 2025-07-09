import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock para window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // Deprecated
    removeListener: vi.fn(), // Deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock para IntersectionObserver
globalThis.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};

// Mock para ResizeObserver
globalThis.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};

// Mock para WebSocket
globalThis.WebSocket = class WebSocket {
  constructor(url) {
    this.url = url;
    this.readyState = WebSocket.CONNECTING;
    setTimeout(() => {
      this.readyState = WebSocket.OPEN;
      if (this.onopen) this.onopen();
    }, 100);
  }
  
  send(data) {
    setTimeout(() => {
      if (this.onmessage) {
        this.onmessage({ data: JSON.stringify({ type: 'mock', data }) });
      }
    }, 100);
  }
  
  close() {
    this.readyState = WebSocket.CLOSED;
    if (this.onclose) this.onclose();
  }
  
  static CONNECTING = 0;
  static OPEN = 1;
  static CLOSING = 2;
  static CLOSED = 3;
};

// Mock para localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};
globalThis.localStorage = localStorageMock;
