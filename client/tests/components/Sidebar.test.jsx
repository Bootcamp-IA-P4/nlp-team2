import React from 'react';
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Sidebar from "../../src/components/Sidebar.jsx";

describe("Sidebar Component", () => {
  const mockSetActiveTab = vi.fn();
  const defaultProps = {
    activeTab: "analyze",
    setActiveTab: mockSetActiveTab,
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should call setActiveTab when clicking on guide tab", () => {
    render(<Sidebar {...defaultProps} />);

    fireEvent.click(screen.getByText("Guía"));
    expect(mockSetActiveTab).toHaveBeenCalledWith("guide");
  });

  it("should call setActiveTab when clicking on history tab", () => {
    render(<Sidebar {...defaultProps} />);

    fireEvent.click(screen.getByText("Historial"));
    expect(mockSetActiveTab).toHaveBeenCalledWith("history");
  });



});
