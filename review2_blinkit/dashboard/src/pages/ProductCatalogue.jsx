import React, { useState } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';
import { CATEGORY_STATS } from '../data/projectData';
import { Search, Tag, DollarSign, Layers } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const SAMPLE_SKUS = [
  { id: 'BLK-001', name: "Baker's Dozen Malabar Paratha", category: 'Frozen Foods', mrp: 165, price: 135, discount: 18.2, stock: 'In Stock' },
  { id: 'BLK-002', name: 'Aashirvaad Malabar Paratha', category: 'Frozen Foods', mrp: 180, price: 145, discount: 19.4, stock: 'In Stock' },
  { id: 'BLK-003', name: 'Amul Taaza Homogenised Toned Milk', category: 'Dairy & Beverages', mrp: 74, price: 74, discount: 0.0, stock: 'In Stock' },
  { id: 'BLK-004', name: 'Mother Dairy Cow Milk 500ml', category: 'Dairy & Beverages', mrp: 28, price: 28, discount: 0.0, stock: 'In Stock' },
  { id: 'BLK-005', name: 'English Oven 100% Atta Bread', category: 'Breakfast Staples', mrp: 55, price: 50, discount: 9.1, stock: 'In Stock' },
  { id: 'BLK-006', name: 'Kettle Studio Potato Chips Crushed Paprika', category: 'Snacks', mrp: 99, price: 79, discount: 20.2, stock: 'In Stock' },
  { id: 'BLK-007', name: '7UP Nimbooz with Lemon Juice', category: 'Beverages', mrp: 40, price: 34, discount: 15.0, stock: 'In Stock' },
  { id: 'BLK-008', name: 'Hybrid Tomato 500g', category: 'Fresh Produce', mrp: 35, price: 29, discount: 17.1, stock: 'In Stock' },
  { id: 'BLK-009', name: 'Fresh Spring Onion 250g', category: 'Fresh Produce', mrp: 25, price: 20, discount: 20.0, stock: 'In Stock' },
  { id: 'BLK-010', name: 'McCain French Fries Crispy Veg', category: 'Frozen Foods', mrp: 145, price: 119, discount: 17.9, stock: 'In Stock' },
  { id: 'BLK-011', name: 'Tata Tea Gold Leaf Tea 500g', category: 'Breakfast Staples', mrp: 310, price: 265, discount: 14.5, stock: 'In Stock' },
  { id: 'BLK-012', name: 'Maggi 2-Minute Instant Noodles 12-Pack', category: 'Instant Foods', mrp: 168, price: 142, discount: 15.5, stock: 'In Stock' },
];

export default function ProductCatalogue() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCat, setSelectedCat] = useState('All');
  const { theme, chartColors } = useTheme();

  const filteredSkus = SAMPLE_SKUS.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          item.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCat = selectedCat === 'All' || item.category === selectedCat;
    return matchesSearch && matchesCat;
  });

  return (
    <div>
      <div className="page-header">
        <span className="page-tag">Catalogue Asset</span>
        <h2>Product Assortment & Pricing Analysis</h2>
        <p>
          Assortment profile of 609 cleaned Blinkit SKUs across 16 commercial categories.
          Collected via automated web scraping and audited for legal MRP compliance.
        </p>
      </div>

      {/* Overview Stat Cards */}
      <div className="grid-3" style={{ marginBottom: '24px' }}>
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ padding: '12px', background: 'var(--accent-secondary-dim)', borderRadius: '10px' }}>
            <Layers size={22} color="var(--accent-secondary)" />
          </div>
          <div>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Assortment Breadth</div>
            <div style={{ fontSize: '24px', fontWeight: '800', color: 'var(--text-primary)' }}>609 SKUs</div>
            <div style={{ fontSize: '11.5px', color: 'var(--blinkit-green)', fontWeight: '600' }}>135 duplicates sanitized</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ padding: '12px', background: 'var(--blinkit-green-bg)', borderRadius: '10px' }}>
            <DollarSign size={22} color="var(--blinkit-green)" />
          </div>
          <div>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Average Selling Price</div>
            <div style={{ fontSize: '24px', fontWeight: '800', color: 'var(--text-primary)' }}>₹98.40</div>
            <div style={{ fontSize: '11.5px', color: 'var(--text-muted)' }}>Average MRP: ₹116.80</div>
          </div>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ padding: '12px', background: 'var(--blinkit-yellow-bg)', borderRadius: '10px' }}>
            <Tag size={22} color="var(--blinkit-yellow)" />
          </div>
          <div>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Average Discount Depth</div>
            <div style={{ fontSize: '24px', fontWeight: '800', color: 'var(--text-primary)' }}>15.7%</div>
            <div style={{ fontSize: '11.5px', color: 'var(--blinkit-yellow)', fontWeight: '600' }}>Peak: 45% (Snacks)</div>
          </div>
        </div>
      </div>

      {/* Category Charts */}
      <div className="grid-2" style={{ marginBottom: '24px' }}>
        <div className="card">
          <div className="card-title" style={{ marginBottom: '14px' }}>MRP vs Selling Price by Category (₹)</div>
          <div style={{ height: '240px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={CATEGORY_STATS} margin={{ top: 10, right: 20, left: -10, bottom: 35 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={chartColors.grid} vertical={false} />
                <XAxis dataKey="category" stroke={chartColors.axisText} angle={-30} textAnchor="end" tick={{ fill: chartColors.axisText, fontSize: 9.5 }} interval={0} />
                <YAxis stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} unit="₹" />
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
                <Bar dataKey="avgMrp" name="Avg MRP (₹)" fill={theme === 'light' ? '#94a3b8' : '#475569'} radius={[3, 3, 0, 0]} />
                <Bar dataKey="avgPrice" name="Avg Selling Price (₹)" fill="var(--blinkit-green)" radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <div className="card-title" style={{ marginBottom: '14px' }}>Average Discount Depth by Category (%)</div>
          <div style={{ height: '240px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={CATEGORY_STATS} margin={{ top: 10, right: 20, left: -10, bottom: 35 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={chartColors.grid} vertical={false} />
                <XAxis dataKey="category" stroke={chartColors.axisText} angle={-30} textAnchor="end" tick={{ fill: chartColors.axisText, fontSize: 9.5 }} interval={0} />
                <YAxis stroke={chartColors.axisText} tick={{ fill: chartColors.axisText, fontSize: 11 }} unit="%" domain={[0, 25]} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: chartColors.tooltipBg, 
                    borderColor: chartColors.tooltipBorder, 
                    color: chartColors.tooltipText, 
                    borderRadius: '8px', 
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)' 
                  }}
                />
                <Bar dataKey="discount" name="Discount (%)" fill="var(--accent-secondary)" radius={[4, 4, 0, 0]}>
                  {CATEGORY_STATS.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.discount > 16 ? 'var(--blinkit-yellow)' : 'var(--accent-secondary)'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Catalogue Filter & Table */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', backgroundColor: 'var(--bg-primary)', padding: '8px 14px', borderRadius: '8px', border: '1px solid var(--border)' }}>
            <Search size={16} color="var(--text-muted)" />
            <input 
              type="text" 
              placeholder="Search SKU name or ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ background: 'transparent', border: 'none', color: 'var(--text-primary)', outline: 'none', fontSize: '13px', width: '220px' }}
            />
          </div>

          <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
            {['All', 'Frozen Foods', 'Dairy & Beverages', 'Breakfast Staples', 'Snacks', 'Fresh Produce'].map(cat => (
              <button
                key={cat}
                onClick={() => setSelectedCat(cat)}
                className={`model-tab-btn ${selectedCat === cat ? 'active' : ''}`}
                style={{ padding: '4px 10px', fontSize: '11.5px' }}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>SKU Identifier</th>
                <th>Product Description</th>
                <th>Assortment Category</th>
                <th>MRP (₹)</th>
                <th>Selling Price (₹)</th>
                <th>Discount Depth</th>
                <th>Availability</th>
              </tr>
            </thead>
            <tbody>
              {filteredSkus.map((item) => (
                <tr key={item.id}>
                  <td><code>{item.id}</code></td>
                  <td style={{ fontWeight: '600' }}>{item.name}</td>
                  <td><span className="badge badge-blue">{item.category}</span></td>
                  <td style={{ textDecoration: item.discount > 0 ? 'line-through' : 'none', color: item.discount > 0 ? 'var(--text-muted)' : 'inherit' }}>
                    ₹{item.mrp}
                  </td>
                  <td style={{ color: 'var(--blinkit-green)', fontWeight: '700' }}>₹{item.price}</td>
                  <td>
                    {item.discount > 0 ? (
                      <span className="badge badge-green">-{item.discount.toFixed(1)}%</span>
                    ) : (
                      <span style={{ fontSize: '11.5px', color: 'var(--text-muted)' }}>0% (Base MRP)</span>
                    )}
                  </td>
                  <td><span style={{ color: 'var(--blinkit-green)', fontSize: '11.5px', fontWeight: '600' }}>● {item.stock}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
