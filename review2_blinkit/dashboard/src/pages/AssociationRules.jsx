import React, { useState } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { ASSOCIATION_RULES, ALGORITHM_BENCHMARK } from '../data/projectData';
import { ShoppingBag, Sliders, Zap, CheckCircle2, PackageCheck } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function AssociationRules() {
  const [minLift, setMinLift] = useState(1.5);
  const [selectedTheme, setSelectedTheme] = useState('All');
  const { theme, chartColors } = useTheme();

  const themes = ['All', ...new Set(ASSOCIATION_RULES.map(r => r.theme))];

  const filteredRules = ASSOCIATION_RULES.filter(rule => {
    const matchesLift = rule.lift >= minLift;
    const matchesTheme = selectedTheme === 'All' || rule.theme === selectedTheme;
    return matchesLift && matchesTheme;
  });

  return (
    <div>
      <div className="page-header">
        <span className="page-tag">Unit 3 Method 2</span>
        <h2>Market Basket Analysis & Bundle Discovery</h2>
        <p>
          Discovered cross-category product affinities across 30,296 multi-item transactions.
          Benchmarked runtime scalability between Apriori and FP-Growth, identifying 42 actionable commercial bundles.
        </p>
      </div>

      {/* Filter Toolbar */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <Sliders size={20} color="var(--accent-secondary)" />
            <div>
              <div style={{ fontSize: '13px', fontWeight: '700', color: 'var(--text-primary)' }}>
                Minimum Lift Filter: <span style={{ color: 'var(--blinkit-green)', fontSize: '15px' }}>{minLift.toFixed(2)}×</span>
              </div>
              <input 
                type="range" 
                min="1.15" 
                max="5.0" 
                step="0.05"
                value={minLift}
                onChange={(e) => setMinLift(parseFloat(e.target.value))}
                style={{ width: '220px', cursor: 'pointer', accentColor: 'var(--blinkit-green)', marginTop: '6px' }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ fontSize: '13px', color: 'var(--text-secondary)', fontWeight: '600' }}>Theme:</span>
            <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
              {themes.map(t => (
                <button
                  key={t}
                  onClick={() => setSelectedTheme(t)}
                  className={`model-tab-btn ${selectedTheme === t ? 'active' : ''}`}
                  style={{ padding: '4px 10px', fontSize: '11.5px' }}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            Showing <strong>{filteredRules.length}</strong> of {ASSOCIATION_RULES.length} mined bundles
          </div>
        </div>
      </div>

      {/* Rules Table */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-title" style={{ marginBottom: '14px' }}>Mined Cross-Category Product Bundles</div>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Trigger Product (Antecedent)</th>
                <th>Recommended Product (Consequent)</th>
                <th>Category Theme</th>
                <th>Support</th>
                <th>Confidence</th>
                <th>Lift Factor</th>
                <th>Operational Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredRules.map((rule, idx) => (
                <tr key={idx}>
                  <td style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{rule.antecedent}</td>
                  <td style={{ color: 'var(--blinkit-green)', fontWeight: '600' }}>+ {rule.consequent}</td>
                  <td>
                    <span className="badge badge-purple">{rule.theme}</span>
                  </td>
                  <td>{rule.support.toFixed(2)}%</td>
                  <td>{rule.confidence.toFixed(2)}%</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <strong style={{ color: rule.lift > 2.5 ? 'var(--blinkit-green)' : rule.lift > 1.8 ? 'var(--accent-amber)' : 'var(--accent-secondary)' }}>
                        {rule.lift.toFixed(2)}×
                      </strong>
                      <div className="lift-bar" style={{ width: '60px' }}>
                        <div 
                          className="lift-fill" 
                          style={{ 
                            width: `${Math.min(100, (rule.lift / 5.2) * 100)}%`,
                            backgroundColor: rule.lift > 2.5 ? 'var(--blinkit-green)' : rule.lift > 1.8 ? 'var(--accent-amber)' : 'var(--accent-secondary)'
                          }}
                        />
                      </div>
                    </div>
                  </td>
                  <td>
                    <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                      {rule.lift > 2.5 ? '1-Click Add-on Banner' : rule.lift > 1.8 ? 'Physical Rack Co-locate' : 'Cart Recommendation'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Algorithm Benchmark & Operational Insights */}
      <div className="grid-2">
        <div className="card">
          <div className="card-title" style={{ marginBottom: '8px' }}>Algorithm Benchmark: Execution Time (Seconds)</div>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '14px' }}>
            Apriori vs FP-Growth runtime across varying support thresholds on 30,296 transactions.
          </p>
          <div style={{ height: '220px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={ALGORITHM_BENCHMARK} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={chartColors.grid} vertical={false} />
                <XAxis dataKey="support" stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} label={{ value: 'Min Support Threshold', position: 'insideBottom', offset: -5, fill: chartColors.axisText, fontSize: 10 }} />
                <YAxis stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} unit="s" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: chartColors.tooltipBg, 
                    borderColor: chartColors.tooltipBorder, 
                    color: chartColors.tooltipText, 
                    borderRadius: '8px', 
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)' 
                  }}
                />
                <Legend verticalAlign="top" height={30} />
                <Bar dataKey="apriori" name="Apriori Algorithm (s)" fill="var(--accent-red)" radius={[4, 4, 0, 0]} />
                <Bar dataKey="fpgrowth" name="FP-Growth Tree (s)" fill="var(--blinkit-green)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <div className="card-title" style={{ marginBottom: '14px' }}>Dark Store Operational Directives</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{ display: 'flex', gap: '10px' }}>
              <PackageCheck size={20} color="var(--blinkit-green)" style={{ flexShrink: 0, marginTop: '2px' }} />
              <div>
                <strong style={{ fontSize: '13px', color: 'var(--text-primary)' }}>Micro-Warehouse Shelf Co-Location</strong>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                  Pairing <em>Baker's Dozen</em> and <em>Aashirvaad Parathas</em> on adjacent freezer shelves reduces picker transit distance by ~14 seconds per multi-item order.
                </p>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <Zap size={20} color="var(--accent-amber)" style={{ flexShrink: 0, marginTop: '2px' }} />
              <div>
                <strong style={{ fontSize: '13px', color: 'var(--text-primary)' }}>Checkout Cart Cross-Selling</strong>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                  Prompting <em>7UP Nimbooz</em> when <em>Kettle Studio Chips</em> is added to the cart yields 32.6% conversion confidence with 1.87× lift.
                </p>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <CheckCircle2 size={20} color="var(--accent-secondary)" style={{ flexShrink: 0, marginTop: '2px' }} />
              <div>
                <strong style={{ fontSize: '13px', color: 'var(--text-primary)' }}>Dynamic Cart Combo Discounting</strong>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                  A nominal 5% combo incentive on high-lift companion items expands Average Order Value (AOV) by an estimated ₹42 across peak weekend hours.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
