import React, { useState } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, Cell
} from 'recharts';
import { MODEL_COMPARISON, FEATURE_IMPORTANCE, FORECAST_SERIES } from '../data/projectData';
import { CheckCircle2, TrendingUp, Sliders, ShieldCheck } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function Forecasting() {
  const [selectedModel, setSelectedModel] = useState('xgboost');
  const { theme, chartColors } = useTheme();

  const modelColors = {
    xgboost: theme === 'light' ? '#0c831f' : '#22c55e',
    sarima: theme === 'light' ? '#2563eb' : '#3b82f6',
    holtWinters: theme === 'light' ? '#d97706' : '#f59e0b',
    movingAvg: theme === 'light' ? '#0891b2' : '#06b6d4',
    seasonalNaive: theme === 'light' ? '#be185d' : '#ec4899',
    naive: theme === 'light' ? '#dc2626' : '#ef4444'
  };

  return (
    <div>
      <div className="page-header">
        <span className="page-tag">Unit 3 Method 1</span>
        <h2>Time-Series Demand Forecasting</h2>
        <p>
          Comparative evaluation of 6 competitive forecasting models on a 30-day chronological holdout horizon (September 2026).
          Features incorporate 14 calendar signals, lag indicators (1, 2, 7, 14 days), and backward rolling statistics.
        </p>
      </div>

      {/* Model Selection Tabs & Line Chart */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px', marginBottom: '18px' }}>
          <div>
            <h3 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }}>
              30-Day Holdout Forecast vs Ground Truth Demand
            </h3>
            <p style={{ fontSize: '12.5px', color: 'var(--text-muted)' }}>
              Select a model architecture to overlay its predictions against actual daily volume
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
            <LineChart data={FORECAST_SERIES} margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke={chartColors.grid} vertical={false} />
              <XAxis dataKey="date" stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} />
              <YAxis stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} domain={['dataMin - 50', 'dataMax + 50']} />
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
                name="Actual Daily Demand" 
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
          <div className="card-title" style={{ marginBottom: '14px' }}>Model Comparison Leaderboard</div>
          <div className="table-container">
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
          </div>
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
