import React from 'react';
import { Table } from 'lucide-react';

const DataTable = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="card" data-testid="data-table">
        <h3>
          <Table />
          Data Preview
        </h3>
        <div className="no-data">No data to display</div>
      </div>
    );
  }

  const headers = Object.keys(data[0]);

  return (
    <div className="card" data-testid="data-table">
      <h3>
        <Table />
        Data Preview (First 20 Rows)
      </h3>
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              {headers.map((key) => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i}>
                {headers.map((key) => (
                  <td key={key}>
                    {row[key] === null || row[key] === 'NaN' || row[key] === '' ? (
                      <span className="missing-val" data-testid="missing-cell">MISSING</span>
                    ) : (
                      String(row[key])
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;
