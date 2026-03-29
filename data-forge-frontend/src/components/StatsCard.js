import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { Activity } from 'lucide-react';

const StatsCard = ({ score, stats }) => {
  const scoreClass = score >= 80 ? 'health-good' : score >= 50 ? 'health-warning' : 'health-bad';
  const statusText = score >= 80 ? 'Excellent' : score >= 50 ? 'Needs Attention' : 'Poor Quality';

  // Prepare data for circular progress (pie chart)
  const progressData = [
    { name: 'Score', value: score },
    { name: 'Remaining', value: 100 - score }
  ];

  const COLORS = [
    score >= 80 ? '#059669' : score >= 50 ? '#d97706' : '#dc2626',
    '#e2e8f0'
  ];

  return (
    <div className="card stats-card" data-testid="stats-card">
      <h3>
        <Activity />
        Data Quality
      </h3>
      <div className="score-container">
        <div className="score-label">Quality Score</div>
        <div className="score-circle">
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie
                data={progressData}
                cx="50%"
                cy="50%"
                startAngle={90}
                endAngle={-270}
                innerRadius={50}
                outerRadius={68}
                dataKey="value"
                stroke="none"
                isAnimationActive={true}
              >
                {progressData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          <div className={`score-value ${scoreClass}`} data-testid="quality-score">
            {score}%
          </div>
        </div>
        <div className={`score-status ${scoreClass}`} data-testid="quality-status">
          {statusText}
        </div>
      </div>

      <div>
        <h3 style={{ marginTop: '16px' }}>Dataset Summary</h3>
        <ul className="summary-list">
          <li className="summary-item">
            <span className="summary-label">Total Rows</span>
            <span className="summary-value" data-testid="total-rows">{stats.rows.toLocaleString()}</span>
          </li>
          <li className="summary-item">
            <span className="summary-label">Total Columns</span>
            <span className="summary-value" data-testid="total-columns">{stats.columns}</span>
          </li>
          <li className="summary-item">
            <span className="summary-label">Missing Values</span>
            <span className="summary-value" style={{ color: stats.missing > 0 ? '#dc2626' : '#059669' }} data-testid="missing-values">
              {stats.missing.toLocaleString()}
            </span>
          </li>
          <li className="summary-item">
            <span className="summary-label">Duplicate Rows</span>
            <span className="summary-value" data-testid="duplicate-rows">{stats.duplicates || 0}</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default StatsCard;
