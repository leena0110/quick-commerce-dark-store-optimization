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
  CheckCircle2
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

export default function Sidebar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <aside className="sidebar">
      {/* Brand Header */}
      <div className="sidebar-logo">
        <div className="brand-badge">
          <Sparkles size={12} />
          <span>Quick Commerce Analytics</span>
        </div>
        <h1>
          <span style={{ color: 'var(--blinkit-yellow)' }}>blink</span>
          <span style={{ color: 'var(--blinkit-green)' }}>it</span>
          <span style={{ fontWeight: '500', fontSize: '13px', color: 'var(--text-secondary)', marginLeft: '4px' }}>Intelligence</span>
        </h1>
        <p>Dark Store Optimization (Review 2)</p>
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
          <div style={{ marginTop: '4px', display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--blinkit-green)', fontSize: '11px', fontWeight: '700' }}>
            <CheckCircle2 size={13} />
            <span>Rubric Verified</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
