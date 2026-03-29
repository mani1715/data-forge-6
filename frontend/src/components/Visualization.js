import React from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { BarChart3, PieChart as PieChartIcon, CheckCircle } from 'lucide-react';

const Visualization = ({ data }) => {
  if (!data) return null;

  const COLORS = ['#0f172a', '#D90429', '#64748b', '#94a3b8', '#cbd5e1'];

  return (
    <div className="visualization-panel">
      {/* Bar Chart: Missing Values */}
      <div className="chart-container" data-testid="missing-chart">
        <div className="chart-title">
          <BarChart3 size={16} />
          Missing Values per Column
        </div>
        {data.missing_data && data.missing_data.length > 0 ? (
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data.missing_data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis 
                dataKey="name" 
                tick={{ fontSize: 11, fill: '#64748b' }}
                angle={-45}
                textAnchor="end"
                height={70}
              />
              <YAxis tick={{ fontSize: 11, fill: '#64748b' }} />
              <Tooltip 
                contentStyle={{ 
                  background: '#FFFFFF', 
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                  fontSize: '13px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
              />
              <Bar dataKey="missing" fill="#D90429" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div style={{ 
            padding: '40px', 
            textAlign: 'center',
            color: '#059669',
            fontWeight: 500,
            fontSize: '14px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px'
          }}>
            <CheckCircle size={18} />
            No Missing Values Found!
          </div>
        )}
      </div>

      {/* Pie Chart: Data Types */}
      <div className="chart-container" data-testid="type-chart">
        <div className="chart-title">
          <PieChartIcon size={16} />
          Data Type Distribution
        </div>
        {data.type_data && data.type_data.length > 0 ? (
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={data.type_data}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={70}
                fill="#8884d8"
                dataKey="value"
              >
                {data.type_data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  background: '#FFFFFF', 
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                  fontSize: '13px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <div className="no-data">No data type information available</div>
        )}
      </div>
    </div>
  );
};

export default Visualization;
