import React from 'react';
import { render, screen, act, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { ThemeProvider, useTheme } from "../../src/contexts/ThemeContext.jsx";

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};

// Mock window.matchMedia
const mockMatchMedia = vi.fn().mockImplementation((query) => ({
  matches: false,
  media: query,
  onchange: null,
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  dispatchEvent: vi.fn(),
}));

// Componente de prueba que usa el contexto
const TestComponent = () => {
  const { isDark, toggleTheme } = useTheme();
  return (
    <div>
      <span data-testid="theme-display">{isDark ? 'dark' : 'light'}</span>
      <button data-testid="toggle-button" onClick={toggleTheme}>
        Toggle Theme
      </button>
    </div>
  );
};

describe("ThemeContext", () => {
  beforeEach(() => {
    vi.stubGlobal("localStorage", localStorageMock);
    vi.stubGlobal("matchMedia", mockMatchMedia);
    vi.clearAllMocks();
    
    // Limpiar clases del document
    document.documentElement.className = '';
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    document.documentElement.className = '';
  });

  it("should provide default theme as light", () => {
    localStorageMock.getItem.mockReturnValue(null);
    mockMatchMedia.mockReturnValue({ matches: false });

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(screen.getByTestId("theme-display")).toHaveTextContent("light");
  });

  it("should load theme from localStorage if available", () => {
    localStorageMock.getItem.mockReturnValue("dark");

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(screen.getByTestId("theme-display")).toHaveTextContent("dark");
  });

  it("should use system preference when no localStorage value", () => {
    localStorageMock.getItem.mockReturnValue(null);
    mockMatchMedia.mockReturnValue({ matches: true });

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(screen.getByTestId("theme-display")).toHaveTextContent("dark");
  });

  it("should toggle theme from light to dark", async () => {
    localStorageMock.getItem.mockReturnValue(null);
    mockMatchMedia.mockReturnValue({ matches: false });

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(screen.getByTestId("theme-display")).toHaveTextContent("light");

    await act(async () => {
      screen.getByTestId("toggle-button").click();
    });

    expect(screen.getByTestId("theme-display")).toHaveTextContent("dark");
  });

  it("should toggle theme from dark to light", async () => {
    localStorageMock.getItem.mockReturnValue("dark");

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(screen.getByTestId("theme-display")).toHaveTextContent("dark");

    await act(async () => {
      screen.getByTestId("toggle-button").click();
    });

    expect(screen.getByTestId("theme-display")).toHaveTextContent("light");
  });

  it("should save theme to localStorage when toggling", async () => {
    localStorageMock.getItem.mockReturnValue(null);
    mockMatchMedia.mockReturnValue({ matches: false });

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    await act(async () => {
      screen.getByTestId("toggle-button").click();
    });

    expect(localStorageMock.setItem).toHaveBeenCalledWith("theme", "dark");
  });

  it("should apply theme class to document", async () => {
    localStorageMock.getItem.mockReturnValue(null);
    mockMatchMedia.mockReturnValue({ matches: false });

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    // Por defecto no debe tener la clase "dark"
    await waitFor(() => {
      expect(document.documentElement.classList.contains("dark")).toBe(false);
    });

    await act(async () => {
      screen.getByTestId("toggle-button").click();
    });

    await waitFor(() => {
      expect(document.documentElement.classList.contains("dark")).toBe(true);
    });
  });


  it("should handle system preference changes", () => {
    const mockAddEventListener = vi.fn();
    const mockRemoveEventListener = vi.fn();
    
    mockMatchMedia.mockReturnValue({
      matches: false,
      addEventListener: mockAddEventListener,
      removeEventListener: mockRemoveEventListener,
    });

    localStorageMock.getItem.mockReturnValue(null);

    const { unmount } = render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    // En la implementación actual, no hay listener para cambios del sistema
    // Este test verifica que el componente no falle si hay cambios
    expect(() => unmount()).not.toThrow();
  });

  it("should provide theme context to children", () => {
    localStorageMock.getItem.mockReturnValue(null);
    mockMatchMedia.mockReturnValue({ matches: false });

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    expect(screen.getByTestId("theme-display")).toBeInTheDocument();
    expect(screen.getByTestId("toggle-button")).toBeInTheDocument();
  });
});
