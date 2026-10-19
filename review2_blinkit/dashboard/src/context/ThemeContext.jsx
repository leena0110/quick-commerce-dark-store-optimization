import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('blinkit_theme') || 'light';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('blinkit_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  };

  // Dynamic colors for Recharts based on current theme
  const chartColors = {
    grid: theme === 'light' ? '#e2e8f0' : '#334155',
    axisText: theme === 'light' ? '#64748b' : '#94a3b8',
    tooltipBg: theme === 'light' ? '#ffffff' : '#1e293b',
    tooltipBorder: theme === 'light' ? '#e2e8f0' : '#475569',
    tooltipText: theme === 'light' ? '#0f172a' : '#f8fafc',
    primary: theme === 'light' ? '#0c831f' : '#22c55e',
    secondary: theme === 'light' ? '#2563eb' : '#3b82f6',
    accent: theme === 'light' ? '#d97706' : '#f59e0b',
    barFill: theme === 'light' ? '#2563eb' : '#3b82f6',
    actualLine: theme === 'light' ? '#0f172a' : '#f8fafc',
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, chartColors }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
