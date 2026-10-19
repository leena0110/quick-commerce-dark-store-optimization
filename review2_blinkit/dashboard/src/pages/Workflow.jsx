import React from 'react';
import { WORKFLOW_STEPS } from '../data/projectData';
import { FileCode, CheckCircle2, Terminal } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function Workflow() {
  const { theme } = useTheme();

  return (
    <div>
      <div className="page-header">
        <span className="page-tag">System Architecture</span>
        <h2>End-to-End Pipeline Workflow</h2>
        <p>
          Stage-by-stage architecture detailing how raw product observations are collected, verified, 
          modelled, and transformed into production analytics, reports, and PowerPoint deliverables.
        </p>
      </div>

      <div className="card" style={{ marginBottom: '24px', backgroundColor: 'var(--accent-secondary-dim)', borderColor: 'rgba(37, 99, 235, 0.25)' }}>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <Terminal size={22} color="var(--accent-secondary)" />
          <div>
            <h4 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--text-primary)' }}>Sequential Pipeline Execution</h4>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
              Every script in <code>review2_blinkit/src/</code> is designed to be fully reproducible and modular. 
              Outputs from each upstream phase feed directly into downstream analytics without hardcoding.
            </p>
          </div>
        </div>
      </div>

      {/* Timeline Steps */}
      <div className="workflow-timeline">
        {WORKFLOW_STEPS.map((step, idx) => (
          <div key={idx} className="workflow-step">
            <div className="step-circle" style={{ borderColor: step.color, color: step.color }}>
              {idx + 1}
            </div>
            
            <div className="card" style={{ flex: 1, borderLeft: `3px solid ${step.color}` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px', marginBottom: '8px' }}>
                <div>
                  <span className="badge" style={{ backgroundColor: `${step.color}18`, color: step.color, marginBottom: '6px' }}>
                    {step.stage}
                  </span>
                  <h3 style={{ fontSize: '16px', fontWeight: '800', color: 'var(--text-primary)' }}>{step.title}</h3>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', backgroundColor: 'var(--bg-primary)', padding: '4px 10px', borderRadius: '6px', border: '1px solid var(--border)' }}>
                  <FileCode size={14} color="var(--accent-secondary)" />
                  <code style={{ fontSize: '11.5px', color: 'var(--text-primary)' }}>{step.file}</code>
                </div>
              </div>

              <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '12px', lineHeight: 1.6 }}>
                {step.desc}
              </p>

              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', backgroundColor: 'var(--bg-primary)', padding: '8px 12px', borderRadius: '8px', border: '1px solid var(--border)' }}>
                <CheckCircle2 size={15} color="var(--blinkit-green)" />
                <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Verified Output:</span>
                <strong style={{ fontSize: '12px', color: 'var(--blinkit-green)' }}>{step.output}</strong>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Data Flow Diagram Card */}
      <div className="card" style={{ marginTop: '24px' }}>
        <div className="card-title" style={{ marginBottom: '14px' }}>Data Artifact Flow Map</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '14px' }}>
          <div style={{ backgroundColor: 'var(--bg-primary)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Ingestion</div>
            <strong style={{ fontSize: '14px', color: 'var(--accent-secondary)' }}>Blinkit Web Catalogue</strong>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              744 raw product DOM elements extracted with BeautifulSoup
            </div>
          </div>

          <div style={{ backgroundColor: 'var(--bg-primary)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Sanitization</div>
            <strong style={{ fontSize: '14px', color: 'var(--blinkit-green)' }}>Clean Catalogue CSV</strong>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              609 verified SKUs, 0 nulls, MRP compliance audited
            </div>
          </div>

          <div style={{ backgroundColor: 'var(--bg-primary)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Grounding</div>
            <strong style={{ fontSize: '14px', color: 'var(--blinkit-yellow)' }}>Bain/Redseer Synthesis</strong>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              106,398 transaction log with diurnal quick-commerce curves
            </div>
          </div>

          <div style={{ backgroundColor: 'var(--bg-primary)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Outputs</div>
            <strong style={{ fontSize: '14px', color: 'var(--accent-purple)' }}>Reports & PPTX</strong>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Automated PowerPoint population & dual-theme dashboard
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
