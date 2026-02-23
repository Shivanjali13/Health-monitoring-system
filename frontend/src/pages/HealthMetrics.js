import React, { useState, useEffect } from 'react';
import { healthAPI } from '../services/api';
import Loading from '../components/Loading';
import './HealthMetrics.css';

const HealthMetrics = () => {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    weight: '',
    blood_pressure_systolic: '',
    blood_pressure_diastolic: '',
    blood_glucose: '',
    heart_rate: '',
    steps: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    setLoading(true);
    try {
      const response = await healthAPI.getMetrics();
      setMetrics(response.data.results || response.data);
    } catch (err) {
      setError('Failed to load metrics');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await healthAPI.createMetric(formData);
      setSuccess('✅ Health metric added successfully!');
      setFormData({
        weight: '',
        blood_pressure_systolic: '',
        blood_pressure_diastolic: '',
        blood_glucose: '',
        heart_rate: '',
        steps: '',
      });
      setShowForm(false);
      fetchMetrics();
    } catch (err) {
      setError('Failed to add metric. Please check all fields.');
    }
  };

  if (loading) return <Loading />;

  return (
    <div className="metrics-container">
      <div className="metrics-header">
        <h1>📊 Health Metrics</h1>
        <button 
          className="add-btn" 
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? '❌ Cancel' : '➕ Add New Metric'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      {showForm && (
        <div className="metric-form-card">
          <h2>Add New Health Metric</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group">
                <label>Weight (kg) *</label>
                <input
                  type="number"
                  step="0.1"
                  name="weight"
                  value={formData.weight}
                  onChange={handleChange}
                  required
                  placeholder="75.5"
                />
              </div>

              <div className="form-group">
                <label>Blood Pressure Systolic (mmHg) *</label>
                <input
                  type="number"
                  name="blood_pressure_systolic"
                  value={formData.blood_pressure_systolic}
                  onChange={handleChange}
                  required
                  placeholder="120"
                />
              </div>

              <div className="form-group">
                <label>Blood Pressure Diastolic (mmHg) *</label>
                <input
                  type="number"
                  name="blood_pressure_diastolic"
                  value={formData.blood_pressure_diastolic}
                  onChange={handleChange}
                  required
                  placeholder="80"
                />
              </div>

              <div className="form-group">
                <label>Blood Glucose (mg/dL) *</label>
                <input
                  type="number"
                  step="0.1"
                  name="blood_glucose"
                  value={formData.blood_glucose}
                  onChange={handleChange}
                  required
                  placeholder="95.5"
                />
              </div>

              <div className="form-group">
                <label>Heart Rate (bpm) *</label>
                <input
                  type="number"
                  name="heart_rate"
                  value={formData.heart_rate}
                  onChange={handleChange}
                  required
                  placeholder="72"
                />
              </div>

              <div className="form-group">
                <label>Steps *</label>
                <input
                  type="number"
                  name="steps"
                  value={formData.steps}
                  onChange={handleChange}
                  required
                  placeholder="8500"
                />
              </div>
            </div>

            <button type="submit" className="submit-btn">
              💾 Save Metric
            </button>
          </form>
        </div>
      )}

      <div className="metrics-list">
        <h2>Your Health History</h2>
        {metrics.length === 0 ? (
          <p className="no-data">No health metrics yet. Add your first entry!</p>
        ) : (
          <div className="metrics-table">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Weight (kg)</th>
                  <th>BP (mmHg)</th>
                  <th>Glucose (mg/dL)</th>
                  <th>Heart Rate (bpm)</th>
                  <th>Steps</th>
                </tr>
              </thead>
              <tbody>
                {metrics.map((metric) => (
                  <tr key={metric.id}>
                    <td>{new Date(metric.recorded_at).toLocaleDateString()}</td>
                    <td>{metric.weight}</td>
                    <td>{metric.blood_pressure_systolic}/{metric.blood_pressure_diastolic}</td>
                    <td>{metric.blood_glucose}</td>
                    <td>{metric.heart_rate}</td>
                    <td>{metric.steps}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default HealthMetrics;