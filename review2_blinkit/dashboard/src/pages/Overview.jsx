import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell
} from 'recharts';
import { KPI_CARDS, MODEL_COMPARISON, CATEGORY_STATS } from '../data/projectData';
import { TrendingUp, ShoppingBag, ArrowRight, CheckCircle2, Layers } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';

const PALETTE = ['#0c831f', '#2563eb', '#f59e0b', '#7c3aed', '#0d9488', '#ea580c', '#0284c7', '#4b5563', '#64748b'];

export default function Overview() {
  const { theme, chartColors } = useTheme();

  return (
    <div>
      {/* Page Header */}
      <div className="page-header">
        <span className="page-tag">Executive Summary</span>
        <h2>Dark Store Inventory & Demand Intelligence</h2>
        <p>
          Integrated business analytics platform leveraging 609 scraped Blinkit product listings, 
          106,398 transaction records, XGBoost time-series forecasting, and FP-Growth co-purchase basket analysis.
        </p>
      </div>

      {/* KPI Grid */}
      <div className="kpi-grid">
        {KPI_CARDS.map((kpi, index) => (
          <div key={index} className="kpi-card" style={{ '--card-accent': kpi.color }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div className="kpi-label">{kpi.label}</div>
            </div>
            <div className="kpi-value">{kpi.value}</div>
            <div className="kpi-sub">{kpi.sub}</div>
          </div>
        ))}
      </div>

      {/* Charts Grid */}
      <div className="grid-2" style={{ marginTop: '24px' }}>
        {/* Model RMSE Comparison */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <div className="card-title">
                <TrendingUp size={16} color="var(--accent-secondary)" />
                Forecast Model Evaluation (RMSE)
              </div>
              <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Holdout evaluation metric (lower is better)</div>
            </div>
            <Link to="/forecasting" style={{ color: 'var(--accent-secondary)', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '4px', textDecoration: 'none', fontWeight: '600' }}>
              Explore <ArrowRight size={14} />
            </Link>
          </div>
          <div style={{ height: '240px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={MODEL_COMPARISON} layout="vertical" margin={{ top: 5, right: 20, left: 30, bottom: 5 }}>
                <XAxis type="number" domain={[0, 160]} stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} />
                <YAxis dataKey="model" type="category" stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} width={95} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: chartColors.tooltipBg, 
                    borderColor: chartColors.tooltipBorder, 
                    color: chartColors.tooltipText, 
                    borderRadius: '8px', 
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)' 
                  }}
                  formatter={(val) => [`${val} RMSE`, 'Score']}
                />
                <Bar dataKey="rmse" radius={[0, 6, 6, 0]}>
                  {MODEL_COMPARISON.map((entry, index) => (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={index === 0 ? 'var(--blinkit-green)' : index === 1 ? 'var(--accent-secondary)' : theme === 'light' ? '#94a3b8' : '#475569'} 
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '10px' }}>
            <strong>XGBoost Regressor</strong> achieved 99.50 RMSE (8.29% WAPE), outperforming the Seasonal-Naive baseline by <strong>27.7%</strong>.
          </div>
        </div>

        {/* Category Breakdown */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <div className="card-title">
                <Layers size={16} color="var(--blinkit-green)" />
                Assortment Depth by Category
              </div>
              <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Assortment breakdown across scraped catalogue</div>
            </div>
            <Link to="/catalogue" style={{ color: 'var(--accent-secondary)', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '4px', textDecoration: 'none', fontWeight: '600' }}>
              Full catalogue <ArrowRight size={14} />
            </Link>
          </div>
          <div style={{ height: '240px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={CATEGORY_STATS} margin={{ top: 5, right: 10, left: -20, bottom: 40 }}>
                <XAxis dataKey="category" stroke={chartColors.axisText} angle={-30} textAnchor="end" interval={0} tick={{ fill: chartColors.axisText, fontSize: 10 }} />
                <YAxis stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: chartColors.tooltipBg, 
                    borderColor: chartColors.tooltipBorder, 
                    color: chartColors.tooltipText, 
                    borderRadius: '8px', 
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)' 
                  }}
                  formatter={(val, name, props) => [`${val} SKUs (Avg disc: ${props.payload.discount}%)`, 'Assortment Count']}
                />
                <Bar dataKey="skus" radius={[4, 4, 0, 0]}>
                  {CATEGORY_STATS.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={PALETTE[index % PALETTE.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '10px' }}>
            Dairy & Beverages leads assortment depth with 95 SKUs, followed by Snacks (78) and Instant Foods (52).
          </div>
        </div>
      </div>

      {/* Review 2 Rubric Compliance Cards */}
      <div className="grid-2" style={{ marginTop: '24px' }}>
        <div className="card" style={{ borderLeft: '4px solid var(--accent-secondary)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <TrendingUp size={18} color="var(--accent-secondary)" />
            <h3 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }}>Unit 3 Method 1: Time-Series Demand Forecasting</h3>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '14px', lineHeight: 1.6 }}>
            Benchmarked 6 models over a rigorous 30-day chronological holdout split without look-ahead data leakage. 
            Engineered 14 lag and rolling window features.
          </p>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <span className="badge badge-green">XGBoost Winner (RMSE 99.50)</span>
            <span className="badge badge-blue">SARIMA (RMSE 99.98)</span>
            <span className="badge badge-amber">WAPE: 8.29%</span>
          </div>
        </div>

        <div className="card" style={{ borderLeft: '4px solid var(--blinkit-green)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <ShoppingBag size={18} color="var(--blinkit-green)" />
            <h3 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }}>Unit 3 Method 2: Association Rule Mining</h3>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '14px', lineHeight: 1.6 }}>
            Synthesized multi-item transactions grounded in Bain (2023) and Redseer (2022) quick-commerce research. 
            Mined 42 cross-category rules with lift up to 5.11× using Apriori and FP-Growth algorithms.
          </p>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <span className="badge badge-green">Top Lift: 5.11×</span>
            <span className="badge badge-purple">42 Rules Mined</span>
            <span className="badge badge-cyan">FP-Growth Benchmarked</span>
          </div>
        </div>
      </div>
    </div>
  );
}
