import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import Sidebar from './components/Sidebar';
import Overview from './pages/Overview';
import Forecasting from './pages/Forecasting';
import AssociationRules from './pages/AssociationRules';
import ProductCatalogue from './pages/ProductCatalogue';
import Workflow from './pages/Workflow';
import Literature from './pages/Literature';
import Recommendations from './pages/Recommendations';

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <ThemeProvider>
      <BrowserRouter>
        <div className="app-layout">
          <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
          <main className={`main-content ${sidebarOpen ? 'sidebar-expanded' : 'sidebar-collapsed'}`}>
            <Routes>
              <Route path="/" element={<Overview />} />
              <Route path="/forecasting" element={<Forecasting />} />
              <Route path="/association-rules" element={<AssociationRules />} />
              <Route path="/catalogue" element={<ProductCatalogue />} />
              <Route path="/workflow" element={<Workflow />} />
              <Route path="/literature" element={<Literature />} />
              <Route path="/recommendations" element={<Recommendations />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </ThemeProvider>
  );
}
