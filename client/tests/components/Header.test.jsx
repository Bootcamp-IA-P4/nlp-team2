import React from 'react';
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Header from "../../src/components/Header.jsx";
import { ThemeProvider } from "../../src/contexts/ThemeContext.jsx";

// Mock del contexto de tema para pruebas controladas
const mockToggleTheme = vi.fn();
const mockTheme = 'light';

// Mock de useTheme hook
vi.mock('../../src/contexts/ThemeContext.jsx', async () => {
  const actual = await vi.importActual('../../src/contexts/ThemeContext.jsx');
  return {
    ...actual,
    useTheme: () => ({
      theme: mockTheme,
      toggleTheme: mockToggleTheme,
    }),
  };
});

describe("Header Component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should render the search input", () => {
    render(
      <ThemeProvider>
        <Header />
      </ThemeProvider>
    );

    const searchInput = screen.getByPlaceholderText("Buscar análisis...");
    expect(searchInput).toBeInTheDocument();
    expect(searchInput).toHaveAttribute("type", "text");
  });

  it("should update search input value when typing", () => {
    render(
      <ThemeProvider>
        <Header />
      </ThemeProvider>
    );

    const searchInput = screen.getByPlaceholderText("Buscar análisis...");
    fireEvent.change(searchInput, { target: { value: "test search" } });

    expect(searchInput).toHaveValue("test search");
  });

  it("should have proper styling classes", () => {
    render(
      <ThemeProvider>
        <Header />
      </ThemeProvider>
    );

    const header = screen.getByRole("banner");
    expect(header).toHaveClass("bg-white");
    expect(header).toHaveClass("shadow-sm");
    expect(header).toHaveClass("border-b");
  });

  it("should be responsive and maintain layout", () => {
    render(
      <ThemeProvider>
        <Header />
      </ThemeProvider>
    );

  });
});
