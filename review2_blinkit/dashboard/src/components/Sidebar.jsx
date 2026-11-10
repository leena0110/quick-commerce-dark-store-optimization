import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  TrendingUp, 
  ShoppingBag, 
  Layers, 
  GitBranch, 
  BookOpen, 
  Lightbulb, 
  Sun,
  Moon,
  Sparkles,
  CheckCircle2,
  Menu,
  ChevronLeft,
  Zap
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const navItems = [
  { path: '/', label: 'Executive Overview', icon: LayoutDashboard },
  { path: '/forecasting', label: 'Demand Forecasting', icon: TrendingUp },
  { path: '/association-rules', label: 'Market Basket Rules', icon: ShoppingBag },
  { path: '/catalogue', label: 'Assortment & Pricing', icon: Layers },
  { path: '/workflow', label: 'Pipeline Architecture', icon: GitBranch },
  { path: '/literature', label: 'Research Matrix', icon: BookOpen },
  { path: '/recommendations', label: 'Dark Store Strategy', icon: Lightbulb },
];

export default function Sidebar({ isOpen, setIsOpen }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <>
      {/* Mobile / Collapsed floating toggle button if closed */}
      {!isOpen && (
        <button 
          className="sidebar-floating-toggle"
          onClick={() => setIsOpen(true)}
          title="Open Navigation Menu"
          aria-label="Open Navigation Menu"
        >
          <Menu size={20} />
        </button>
      )}

      {/* Backdrop overlay for smaller screens */}
      {isOpen && (
        <div 
          className="sidebar-backdrop" 
          onClick={() => setIsOpen(false)} 
        />
      )}

      <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
        {/* Brand Header */}
        <div className="sidebar-logo">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div className="brand-badge">
              <Sparkles size={12} />
              <span>Quick Commerce Analytics</span>
            </div>
            <button 
              className="sidebar-close-btn"
              onClick={() => setIsOpen(!isOpen)}
              title={isOpen ? "Collapse Menu" : "Expand Menu"}
              aria-label="Toggle Navigation Menu"
            >
              <ChevronLeft size={18} />
            </button>
          </div>
          <h1>
            <span style={{ color: 'var(--blinkit-yellow)', display: 'inline-flex', alignItems: 'center', gap: '3px' }}>
              <Zap size={18} fill="var(--blinkit-yellow)" /> Quick
            </span>
            <span style={{ color: 'var(--blinkit-green)' }}>Cast</span>
          </h1>
          <p>Dark Store Optimization & Forecasting</p>
        </div>

      {/* Main Navigation */}
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              <span className="nav-icon"><Icon size={17} /></span>
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Footer & Theme Switcher */}
      <div className="sidebar-footer">
        {/* Theme Toggle Button */}
        <button 
          onClick={toggleTheme} 
          className="theme-toggle-btn"
          title={`Switch to ${theme === 'light' ? 'Dark' : 'Light'} Mode`}
        >
          <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {theme === 'light' ? <Sun size={15} color="#d97706" /> : <Moon size={15} color="#38bdf8" />}
            <span>Theme</span>
          </span>
          <span className="theme-pill">
            {theme === 'light' ? 'Light' : 'Dark'}
          </span>
        </button>

        <div className="sidebar-info">
          <div><strong>Course:</strong> 23CSE452 Business Analytics</div>
          <div>Amrita Vishwa Vidyapeetham</div>
        </div>
      </div>
    </aside>
    </>
  );
}
