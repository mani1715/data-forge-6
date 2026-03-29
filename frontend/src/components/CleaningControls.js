import React from 'react';
import { Settings, Wand2, Trash2, TrendingDown, Type, Sparkles } from 'lucide-react';

const CleaningControls = ({ strategy, setStrategy, onAction, loading, aiMessage }) => {
  return (
    <div className="card" data-testid="cleaning-controls">
      <h3>
        <Settings />
        Cleaning Tools
      </h3>
      
      <div className="controls-section">
        <div className="control-group">
          <label className="control-label">Missing Value Strategy</label>
          <select 
            value={strategy} 
            onChange={(e) => setStrategy(e.target.value)} 
            className="select-dropdown"
            disabled={loading}
            data-testid="strategy-dropdown"
          >
            <option value="ai">AI Prediction (MICE)</option>
            <option value="mean">Mean</option>
            <option value="median">Median</option>
            <option value="mode">Mode</option>
            <option value="constant">Fill with 0</option>
            <option value="drop_rows">Drop Rows</option>
          </select>
        </div>

        <div className="action-buttons">
          <button 
            className="btn btn-primary" 
            onClick={() => onAction('fill_missing')} 
            disabled={loading}
            data-testid="fill-missing-button"
          >
            <Wand2 size={16} />
            Clean Missing Values
          </button>

          <button 
            className="btn btn-secondary" 
            onClick={() => onAction('remove_duplicates')} 
            disabled={loading}
            data-testid="remove-duplicates-button"
          >
            <Trash2 size={16} />
            Remove Duplicates with AI
          </button>

          <button 
            className="btn btn-secondary" 
            onClick={() => onAction('remove_outliers')} 
            disabled={loading}
            data-testid="remove-outliers-button"
          >
            <TrendingDown size={16} />
            Remove Outliers with AI
          </button>

          <button 
            className="btn btn-secondary" 
            onClick={() => onAction('clean_text')} 
            disabled={loading}
            data-testid="clean-text-button"
          >
            <Type size={16} />
            Clean Text Data with AI
          </button>
        </div>

        {aiMessage && (
          <div className="ai-explanation" data-testid="ai-explanation">
            <div className="ai-explanation-header">
              <Sparkles size={16} />
              <span>AI Insights</span>
            </div>
            <div className="ai-explanation-text">{aiMessage}</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CleaningControls;
