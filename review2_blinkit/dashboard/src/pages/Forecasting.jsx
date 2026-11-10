import React, { useState } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, Cell
} from 'recharts';
import { MODEL_COMPARISON, FEATURE_IMPORTANCE, CATEGORY_FORECAST_DATA } from '../data/projectData';
import { CheckCircle2, TrendingUp, Sliders, ShieldCheck, Filter, Calendar, Layers } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function Forecasting() {
  const [selectedModel, setSelectedModel] = useState('xgboost');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [horizonDays, setHorizonDays] = useState(30);
  const [modelTier, setModelTier] = useState('review2'); // 'review2' (aggregate time-series) or 'review1' (granular ML)
  const { theme, chartColors } = useTheme();

  const modelColors = {
    xgboost: theme === 'light' ? '#0c831f' : '#22c55e',
    sarima: theme === 'light' ? '#2563eb' : '#3b82f6',
    holtWinters: theme === 'light' ? '#d97706' : '#f59e0b',
    movingAvg: theme === 'light' ? '#0891b2' : '#06b6d4',
    seasonalNaive: theme === 'light' ? '#be185d' : '#ec4899',
    naive: theme === 'light' ? '#dc2626' : '#ef4444'
  };

  // Slice based on selected category and horizon
  const rawSeries = CATEGORY_FORECAST_DATA[selectedCategory] || CATEGORY_FORECAST_DATA.all;
  const activeSeries = rawSeries.slice(0, horizonDays);

  return (
    <div>
      <div className="page-header">
        <span className="page-tag">Demand Analytics Engine</span>
        <h2>QuickCast Demand Forecasting & Predictive Modeling</h2>
        <p>
          Multi-horizon predictive modeling comparing Review 2 store-level time series algorithms and Review 1 SKU-level supervised regressors.
        </p>
      </div>

      {/* Interactive Controls & Filter Bar */}
      <div className="card" style={{ marginBottom: '20px', padding: '16px 20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          
          {/* Category Dropdown Selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Filter size={16} color="var(--blinkit-green)" />
            <label htmlFor="category-select" style={{ fontSize: '13px', fontWeight: '700', color: 'var(--text-secondary)' }}>
              Category:
            </label>
            <select
              id="category-select"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="custom-select"
            >
              <option value="all">All Store Departments (Aggregate)</option>
              <option value="dairy">Dairy & Fresh Milk</option>
              <option value="snacks">Snacks & Instant Foods</option>
              <option value="produce">Fresh Fruits & Vegetables</option>
              <option value="beverages">Cold Beverages & Juices</option>
            </select>
          </div>

          {/* Time Horizon Selector Dropdown */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Calendar size={16} color="var(--accent-secondary)" />
            <label htmlFor="horizon-select" style={{ fontSize: '13px', fontWeight: '700', color: 'var(--text-secondary)' }}>
              Forecast Horizon:
            </label>
            <select
              id="horizon-select"
              value={horizonDays}
              onChange={(e) => setHorizonDays(Number(e.target.value))}
              className="custom-select"
            >
              <option value={7}>Next 7 Days (Micro-Restock)</option>
              <option value={14}>Next 14 Days (Bi-weekly)</option>
              <option value={30}>Full 30-Day Holdout (September 2026)</option>
            </select>
          </div>

          {/* Modeling Track Switcher (Review 1 vs Review 2) */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Layers size={16} color="var(--accent-amber)" />
            <span style={{ fontSize: '13px', fontWeight: '700', color: 'var(--text-secondary)' }}>Evaluation Tier:</span>
            <div className="model-tabs" style={{ margin: 0 }}>
              <button 
                className={`model-tab-btn ${modelTier === 'review2' ? 'active' : ''}`}
                onClick={() => setModelTier('review2')}
                style={{ padding: '5px 12px', fontSize: '12px' }}
              >
                Review 2 (Time Series)
              </button>
              <button 
                className={`model-tab-btn ${modelTier === 'review1' ? 'active' : ''}`}
                onClick={() => setModelTier('review1')}
                style={{ padding: '5px 12px', fontSize: '12px' }}
              >
                Review 1 (SKU-Level ML)
              </button>
            </div>
          </div>

        </div>
      </div>

      {/* Model Selection Tabs & Line Chart */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px', marginBottom: '18px' }}>
          <div>
            <h3 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }}>
              {horizonDays}-Day Horizon: Actual vs. {selectedModel.toUpperCase()} Prediction
            </h3>
            <p style={{ fontSize: '12.5px', color: 'var(--text-muted)' }}>
              {selectedCategory === 'all' ? 'All Store Volume' : selectedCategory.toUpperCase()} • Filtered to {horizonDays} daily timestamps
            </p>
          </div>
          <div className="model-tabs">
            {[
              { id: 'xgboost', label: 'XGBoost (Winner)' },
              { id: 'sarima', label: 'SARIMA (2nd)' },
              { id: 'holtWinters', label: 'Holt-Winters' },
              { id: 'movingAvg', label: 'Moving Avg 7d' },
              { id: 'seasonalNaive', label: 'Seasonal Naive' },
              { id: 'naive', label: 'Naive (t-1)' }
            ].map(tab => (
              <button
                key={tab.id}
                className={`model-tab-btn ${selectedModel === tab.id ? 'active' : ''}`}
                onClick={() => setSelectedModel(tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Recharts LineChart */}
        <div style={{ height: '320px', width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={activeSeries} margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke={chartColors.grid} vertical={false} />
              <XAxis dataKey="date" stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} />
              <YAxis stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} domain={['dataMin - 30', 'dataMax + 30']} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: chartColors.tooltipBg, 
                  borderColor: chartColors.tooltipBorder, 
                  color: chartColors.tooltipText, 
                  borderRadius: '8px', 
                  boxShadow: '0 4px 12px rgba(0,0,0,0.1)' 
                }}
              />
              <Legend verticalAlign="top" height={36} />
              <Line 
                type="monotone" 
                dataKey="actual" 
                name="Actual Daily Volume" 
                stroke={chartColors.actualLine} 
                strokeWidth={2.5} 
                dot={{ r: 3, fill: chartColors.actualLine }} 
              />
              <Line 
                type="monotone" 
                dataKey={selectedModel} 
                name={`Predicted (${selectedModel.toUpperCase()})`} 
                stroke={modelColors[selectedModel]} 
                strokeWidth={2.5} 
                strokeDasharray="4 2"
                dot={{ r: 3, fill: modelColors[selectedModel] }} 
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Model Benchmark Table and Feature Importance */}
      <div className="grid-2">
        {/* Benchmark Table */}
        <div className="card">
          <div className="card-title" style={{ marginBottom: '14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>{modelTier === 'review2' ? 'Store Demand Leaderboard (Review 2)' : 'SKU-Level ML Benchmarks (Review 1)'}</span>
            <span className="badge badge-purple">{modelTier === 'review2' ? '6 Time-Series Models' : '3 Supervised Regressors'}</span>
          </div>
          <div className="table-container">
            {modelTier === 'review2' ? (
              <table>
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Model Architecture</th>
                    <th>MAE</th>
                    <th>RMSE</th>
                    <th>WAPE (%)</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {MODEL_COMPARISON.map((row) => (
                    <tr key={row.model} style={row.rank === 1 ? { backgroundColor: 'var(--accent-primary-dim)' } : {}}>
                      <td>
                        <span className={`badge ${row.rank === 1 ? 'badge-green' : row.rank <= 3 ? 'badge-blue' : 'badge-amber'}`}>
                          #{row.rank}
                        </span>
                      </td>
                      <td style={{ fontWeight: row.rank === 1 ? '700' : '500', color: row.rank === 1 ? 'var(--blinkit-green)' : 'inherit' }}>
                        {row.model}
                      </td>
                      <td>{row.mae.toFixed(2)}</td>
                      <td style={{ fontWeight: '700' }}>{row.rmse.toFixed(2)}</td>
                      <td>{row.wape.toFixed(2)}%</td>
                      <td>
                        {row.rank === 1 ? (
                          <span style={{ color: 'var(--blinkit-green)', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', fontWeight: '700' }}>
                            <CheckCircle2 size={14} /> Winner
                          </span>
                        ) : (
                          <span style={{ color: 'var(--text-muted)', fontSize: '12px' }}>Benchmark</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Model</th>
                    <th>R² Score</th>
                    <th>MAE (units)</th>
                    <th>RMSE</th>
                    <th>Evaluation Level</th>
                  </tr>
                </thead>
                <tbody>
                  <tr style={{ backgroundColor: 'var(--accent-primary-dim)' }}>
                    <td style={{ fontWeight: '700', color: 'var(--blinkit-green)' }}>Random Forest (Best)</td>
                    <td>0.3710</td>
                    <td style={{ fontWeight: '700' }}>1.3322</td>
                    <td>1.8332</td>
                    <td><span className="badge badge-green">Recommended</span></td>
                  </tr>
                  <tr>
                    <td style={{ fontWeight: '500' }}>XGBoost Regressor</td>
                    <td>0.3684</td>
                    <td>1.3339</td>
                    <td>1.8369</td>
                    <td><span className="badge badge-blue">Competitive</span></td>
                  </tr>
                  <tr>
                    <td style={{ fontWeight: '500' }}>Linear Regression</td>
                    <td>0.3675</td>
                    <td>1.3456</td>
                    <td>1.8383</td>
                    <td><span className="badge badge-amber">Baseline</span></td>
                  </tr>
                </tbody>
              </table>
            )}
          </div>
          {modelTier === 'review1' && (
            <p style={{ fontSize: '11.5px', color: 'var(--text-muted)', marginTop: '10px' }}>
              Target: <code>Daily_Quantity</code> per store-product-day. Tested on 15,776 chronological holdout records.
            </p>
          )}
        </div>

        {/* Feature Importance */}
        <div className="card">
          <div className="card-title" style={{ marginBottom: '14px' }}>XGBoost Relative Feature Importance (%)</div>
          <div style={{ height: '240px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={FEATURE_IMPORTANCE} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                <XAxis type="number" domain={[0, 35]} stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} unit="%" />
                <YAxis dataKey="feature" type="category" stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} width={90} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: chartColors.tooltipBg, 
                    borderColor: chartColors.tooltipBorder, 
                    color: chartColors.tooltipText, 
                    borderRadius: '8px', 
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)' 
                  }}
                  formatter={(val) => [`${val}%`, 'Relative Weight']}
                />
                <Bar dataKey="importance" radius={[0, 4, 4, 0]}>
                  {FEATURE_IMPORTANCE.map((entry, index) => (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={index === 0 ? 'var(--blinkit-green)' : index < 3 ? 'var(--accent-secondary)' : theme === 'light' ? '#94a3b8' : '#475569'} 
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '12px' }}>
            Calendar signals and weekly cyclicality account for over <strong>65%</strong> of total predictive power (<code>day_of_week</code> 31.8%, <code>lag_7</code> 17.6%, <code>is_weekend</code> 16.2%).
          </div>
        </div>
      </div>

      {/* Methodology Alert */}
      <div className="card" style={{ marginTop: '24px', backgroundColor: 'var(--accent-secondary-dim)', borderColor: 'rgba(37, 99, 235, 0.25)' }}>
        <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
          <ShieldCheck size={22} color="var(--accent-secondary)" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div>
            <h4 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '4px' }}>
              Methodological Rigour & Leakage Prevention (M5 Competition Standard)
            </h4>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Following recommendations by <strong>Makridakis et al. (2022)</strong>, evaluation partitioned strictly 
              chronologically: 60 operating days for training and parameter calibration, followed by an unobserved 
              30-day evaluation horizon (September 2026). Rolling statistics and lag features were computed strictly backwards 
              to guarantee zero look-ahead bias.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
