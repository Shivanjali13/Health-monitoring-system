import React, { useState, useEffect } from 'react';
import { analyticsAPI, healthAPI } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Loading from '../components/Loading';
import './Dashboard.css';

const Dashboard = () => {
  const [dashboard, setDashboard] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [dashboardRes, summaryRes] = await Promise.all([
        analyticsAPI.getDashboard(),
        healthAPI.getSummary(),
      ]);
      setDashboard(dashboardRes.data);
      setSummary(summaryRes.data);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="dashboard-container">
      <h1>📊 Health Dashboard</h1>

      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="card card-blue">
          <div className="card-icon">📈</div>
          <div className="card-content">
            <h3>Total Records</h3>
            <p className="card-number">{summary?.total_records || 0}</p>
          </div>
        </div>

        <div className="card card-green">
          <div className="card-icon">💪</div>
          <div className="card-content">
            <h3>Latest Weight</h3>
            <p className="card-number">{summary?.latest_metrics?.weight || 'N/A'} kg</p>
          </div>
        </div>

        <div className="card card-orange">
          <div className="card-icon">⚠️</div>
          <div className="card-content">
            <h3>Active Anomalies</h3>
            <p className="card-number">{dashboard?.active_anomalies || 0}</p>
          </div>
        </div>

        <div className="card card-purple">
          <div className="card-icon">💡</div>
          <div className="card-content">
            <h3>Unread Tips</h3>
            <p className="card-number">{dashboard?.unread_tips || 0}</p>
          </div>
        </div>
      </div>

      {/* Latest Metrics */}
      {summary?.latest_metrics && (
        <div className="dashboard-section">
          <h2>Latest Health Metrics</h2>
          <div className="metrics-grid">
            <div className="metric-card">
              <span className="metric-label">Weight</span>
              <span className="metric-value">{summary.latest_metrics.weight} kg</span>
            </div>
            <div className="metric-card">
              <span className="metric-label">Blood Pressure</span>
              <span className="metric-value">
                {summary.latest_metrics.blood_pressure_systolic}/
                {summary.latest_metrics.blood_pressure_diastolic}
              </span>
            </div>
            <div className="metric-card">
              <span className="metric-label">Blood Glucose</span>
              <span className="metric-value">{summary.latest_metrics.blood_glucose} mg/dL</span>
            </div>
            <div className="metric-card">
              <span className="metric-label">Heart Rate</span>
              <span className="metric-value">{summary.latest_metrics.heart_rate} bpm</span>
            </div>
            <div className="metric-card">
              <span className="metric-label">Steps</span>
              <span className="metric-value">{summary.latest_metrics.steps}</span>
            </div>
          </div>
        </div>
      )}

      {/* Weight Predictions Chart */}
      {dashboard?.weight_predictions && dashboard.weight_predictions.length > 0 && (
        <div className="dashboard-section">
          <h2>Weight Predictions (Next 7 Days)</h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={dashboard.weight_predictions}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="prediction_date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="predicted_weight" 
                  stroke="#667eea" 
                  strokeWidth={2}
                  name="Predicted Weight (kg)"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Diabetes Risk */}
      {dashboard?.diabetes_risk && (
        <div className="dashboard-section">
          <h2>Diabetes Risk Assessment</h2>
          <div className={`risk-card risk-${dashboard.diabetes_risk.risk_level.toLowerCase()}`}>
            <div className="risk-header">
              <h3>Risk Level: {dashboard.diabetes_risk.risk_level}</h3>
              <span className="risk-score">{dashboard.diabetes_risk.risk_score}%</span>
            </div>
            <p className="risk-recommendations">{dashboard.diabetes_risk.recommendations}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;