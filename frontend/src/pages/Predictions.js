import React, { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import Loading from '../components/Loading';
import './Predictions.css';

const Predictions = () => {
  const [weightPrediction, setWeightPrediction] = useState(null);
  const [diabetesRisk, setDiabetesRisk] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchPredictions();
  }, []);

  const fetchPredictions = async () => {
    setLoading(true);
    setError('');
    try {
      const [weightRes, diabetesRes] = await Promise.all([
        analyticsAPI.getWeightPrediction(),
        analyticsAPI.getDiabetesRisk(),
      ]);
      setWeightPrediction(weightRes.data);
      setDiabetesRisk(diabetesRes.data);
    } catch (err) {
      setError('Failed to load predictions. Make sure you have at least 3 health metric entries.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;

  return (
    <div className="predictions-container">
      <h1>🔮 Health Predictions & Analytics</h1>

      {error && <div className="error-message">{error}</div>}

      {/* Weight Prediction Section */}
      {weightPrediction && (
        <div className="prediction-section">
          <h2>📈 Weight Prediction (Next 7 Days)</h2>
          
          <div className="prediction-summary">
            <div className="summary-item">
              <span className="summary-label">Current Weight</span>
              <span className="summary-value">{weightPrediction.current_weight} kg</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Trend</span>
              <span className={`summary-value trend-${weightPrediction.trend}`}>
                {weightPrediction.trend === 'gaining' && '📈 Gaining'}
                {weightPrediction.trend === 'losing' && '📉 Losing'}
                {weightPrediction.trend === 'stable' && '➡️ Stable'}
              </span>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={weightPrediction.predictions}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tickFormatter={(date) => new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                />
                <YAxis 
                  domain={['dataMin - 1', 'dataMax + 1']}
                  label={{ value: 'Weight (kg)', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  labelFormatter={(date) => new Date(date).toLocaleDateString()}
                  formatter={(value, name) => {
                    if (name === 'weight') return [`${value} kg`, 'Predicted Weight'];
                    if (name === 'confidence') return [`${value}%`, 'Confidence'];
                    return [value, name];
                  }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="weight" 
                  stroke="#667eea" 
                  strokeWidth={3}
                  dot={{ fill: '#667eea', r: 5 }}
                  name="Predicted Weight"
                />
                <Line 
                  type="monotone" 
                  dataKey="confidence" 
                  stroke="#48bb78" 
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  name="Confidence %"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="predictions-table">
            <h3>Detailed Predictions</h3>
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Predicted Weight</th>
                  <th>Confidence</th>
                </tr>
              </thead>
              <tbody>
                {weightPrediction.predictions.map((pred, index) => (
                  <tr key={index}>
                    <td>{new Date(pred.date).toLocaleDateString()}</td>
                    <td>{pred.weight} kg</td>
                    <td>
                      <div className="confidence-bar">
                        <div 
                          className="confidence-fill" 
                          style={{ width: `${pred.confidence}%` }}
                        ></div>
                        <span>{pred.confidence}%</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Diabetes Risk Section */}
      {diabetesRisk && (
        <div className="prediction-section">
          <h2>🩺 Diabetes Risk Assessment</h2>
          
          <div className={`risk-banner risk-${diabetesRisk.risk_level.toLowerCase()}`}>
            <div className="risk-info">
              <h3>Risk Level: {diabetesRisk.risk_level}</h3>
              <div className="risk-score-circle">
                <svg viewBox="0 0 100 100">
                  <circle
                    cx="50"
                    cy="50"
                    r="45"
                    fill="none"
                    stroke="#e0e0e0"
                    strokeWidth="10"
                  />
                  <circle
                    cx="50"
                    cy="50"
                    r="45"
                    fill="none"
                    stroke={
                      diabetesRisk.risk_level === 'LOW' ? '#48bb78' :
                      diabetesRisk.risk_level === 'MODERATE' ? '#ed8936' :
                      '#f56565'
                    }
                    strokeWidth="10"
                    strokeDasharray={`${diabetesRisk.risk_score * 2.83} 283`}
                    strokeLinecap="round"
                    transform="rotate(-90 50 50)"
                  />
                </svg>
                <div className="score-text">
                  <span className="score-number">{diabetesRisk.risk_score}</span>
                  <span className="score-label">Score</span>
                </div>
              </div>
            </div>
          </div>

          <div className="risk-factors">
            <h3>Risk Factors Analysis</h3>
            <div className="factors-grid">
              {Object.entries(diabetesRisk.factors).map(([key, value]) => (
                <div key={key} className="factor-card">
                  <h4>{key.toUpperCase()}</h4>
                  <div className="factor-value">
                    {typeof value.value === 'number' ? value.value.toFixed(1) : value.value}
                  </div>
                  <div className="factor-status">
                    Status: <span className={`status-${value.status}`}>{value.status}</span>
                  </div>
                  <div className="factor-score">
                    Risk Score: {value.score.toFixed(0)}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="recommendations-section">
            <h3>📋 Personalized Recommendations</h3>
            <div className="recommendations-text">
              {diabetesRisk.recommendations.split('\n').map((rec, index) => (
                <p key={index}>{rec}</p>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Predictions;