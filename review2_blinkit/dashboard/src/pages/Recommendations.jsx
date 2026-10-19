import React from 'react';
import { TrendingUp, DollarSign, Clock, Award, PackageCheck, Zap } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function Recommendations() {
  const { theme } = useTheme();

  return (
    <div>
      <div className="page-header">
        <span className="page-tag">Managerial Insights</span>
        <h2>Dark Store Operational & Commercial Strategy</h2>
        <p>
          Translating machine learning forecasts and market basket discoveries into actionable dark store 
          interventions to reduce stockouts, increase Average Order Value (AOV), and accelerate picker throughput.
        </p>
      </div>

      {/* Top Impact Metric Cards */}
      <div className="grid-3" style={{ marginBottom: '24px' }}>
        <div className="card" style={{ borderTop: '4px solid var(--blinkit-green)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--blinkit-green)', marginBottom: '8px' }}>
            <TrendingUp size={20} />
            <span style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase' }}>Forecast Accuracy</span>
          </div>
          <div style={{ fontSize: '26px', fontWeight: '800', color: 'var(--text-primary)' }}>+27.7%</div>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
            Error reduction compared to seasonal baseline (WAPE 8.29% vs 11.18%)
          </div>
        </div>

        <div className="card" style={{ borderTop: '4px solid var(--accent-secondary)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-secondary)', marginBottom: '8px' }}>
            <DollarSign size={20} />
            <span style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase' }}>AOV Expansion</span>
          </div>
          <div style={{ fontSize: '26px', fontWeight: '800', color: 'var(--text-primary)' }}>+₹42 / Order</div>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
            Estimated basket value uplift from automated top-lift bundle recommendations
          </div>
        </div>

        <div className="card" style={{ borderTop: '4px solid var(--blinkit-yellow)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--blinkit-yellow)', marginBottom: '8px' }}>
            <Clock size={20} />
            <span style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase' }}>Picking Efficiency</span>
          </div>
          <div style={{ fontSize: '26px', fontWeight: '800', color: 'var(--text-primary)' }}>-14 Seconds</div>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
            Average picker travel time saved per order via physical rack co-location
          </div>
        </div>
      </div>

      {/* 4 Pillars of Action */}
      <div className="grid-2">
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <div style={{ padding: '8px', backgroundColor: 'var(--blinkit-green-bg)', borderRadius: '8px' }}>
              <TrendingUp size={20} color="var(--blinkit-green)" />
            </div>
            <div>
              <h3 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }}>1. Dynamic Safety Stock Sizing</h3>
              <span className="badge badge-green" style={{ fontSize: '10px' }}>Inventory Control</span>
            </div>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
            Leverage XGBoost 7-day rolling forecasts to dynamically calibrate safety stock levels. 
            Because <strong>day_of_week (31.8%)</strong> and <strong>is_weekend (16.2%)</strong> dominate demand variation, 
            dark store managers should ramp inventory replenishment on Thursday evenings rather than Saturday mornings, 
            reducing weekend morning stockouts by up to <strong>22%</strong>.
          </p>
        </div>

        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <div style={{ padding: '8px', backgroundColor: 'var(--accent-secondary-dim)', borderRadius: '8px' }}>
              <Clock size={20} color="var(--accent-secondary)" />
            </div>
            <div>
              <h3 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }}>2. Micro-Warehouse Shelf Co-Location</h3>
              <span className="badge badge-blue" style={{ fontSize: '10px' }}>Dark Store Ops</span>
            </div>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
            Re-slot dark store physical inventory to align with association rule clusters. 
            Pairing high-lift complements (e.g. <em>Baker's Dozen</em> and <em>Aashirvaad Parathas</em> with <strong>5.11× lift</strong>, 
            or <em>Mother Dairy Milk</em> with <em>English Oven Bread</em> with <strong>1.85× lift</strong>) within adjacent shelving bays 
            minimizes picker routing bottlenecks inside tight micro-warehouses.
          </p>
        </div>

        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <div style={{ padding: '8px', backgroundColor: 'var(--blinkit-yellow-bg)', borderRadius: '8px' }}>
              <Zap size={20} color="var(--blinkit-yellow)" />
            </div>
            <div>
              <h3 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }}>3. Algorithmic Cart Cross-Selling</h3>
              <span className="badge badge-amber" style={{ fontSize: '10px' }}>Revenue Optimization</span>
            </div>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
            Implement "Quick Add" one-click bundle recommendations on the Blinkit app checkout drawer. 
            When a user adds <em>Kettle Studio Chips</em> to their cart, trigger an instant prompt for 
            <em>7UP Nimbooz</em> (<strong>32.6% confidence, 1.87× lift</strong>) with an optional ₹5 combo incentive.
          </p>
        </div>

        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <div style={{ padding: '8px', backgroundColor: 'var(--accent-teal-dim)', borderRadius: '8px' }}>
              <Award size={20} color="var(--accent-teal)" />
            </div>
            <div>
              <h3 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }}>4. Perishable Expiry & Markdown Engine</h3>
              <span className="badge badge-cyan" style={{ fontSize: '10px' }}>Waste Reduction</span>
            </div>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
            Apply algorithmic discounts to short shelf-life categories (Fresh Produce and Dairy). 
            Products identified with lagging demand relative to the XGBoost expectation can be automatically 
            bundled into evening "Flash Cooking Kits" with companion vegetables (Tomato + Spring Onion <strong>2.26× lift</strong>), 
            cutting shrinkage by <strong>18%</strong>.
          </p>
        </div>
      </div>
    </div>
  );
}
