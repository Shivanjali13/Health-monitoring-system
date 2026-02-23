import React, { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';
import Loading from '../components/Loading';
import './HealthTips.css';

const HealthTips = () => {
  const [tips, setTips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTips();
  }, []);

  const fetchTips = async () => {
    setLoading(true);
    try {
      const response = await analyticsAPI.getHealthTips();
      setTips(response.data.tips);
    } catch (err) {
      setError('Failed to load health tips');
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (tipId) => {
    try {
      await analyticsAPI.markTipAsRead(tipId);
      setTips(tips.map(tip => 
        tip.id === tipId ? { ...tip, is_read: true } : tip
      ));
    } catch (err) {
      console.error('Failed to mark tip as read');
    }
  };

  const getPriorityColor = (priority) => {
    if (priority >= 4) return 'priority-high';
    if (priority >= 2) return 'priority-medium';
    return 'priority-low';
  };

  const getCategoryIcon = (category) => {
    const icons = {
      weight_management: '⚖️',
      exercise: '🏃',
      blood_pressure: '💗',
      blood_glucose: '🩸',
      heart_health: '❤️',
      general_wellness: '🌟',
      anomaly_alert: '⚠️',
    };
    return icons[category] || '💡';
  };

  if (loading) return <Loading />;

  return (
    <div className="tips-container">
      <h1>💡 Personalized Health Tips</h1>

      {error && <div className="error-message">{error}</div>}

      {tips.length === 0 ? (
        <div className="no-tips">
          <p>✨ No new health tips available.</p>
          <p>Keep logging your health metrics to receive personalized recommendations!</p>
        </div>
      ) : (
        <div className="tips-grid">
          {tips.map((tip) => (
            <div 
              key={tip.id} 
              className={`tip-card ${getPriorityColor(tip.priority)} ${tip.is_read ? 'read' : ''}`}
            >
              <div className="tip-header">
                <span className="tip-icon">{getCategoryIcon(tip.category)}</span>
                <span className="tip-category">{tip.category.replace('_', ' ')}</span>
                <span className={`tip-priority ${getPriorityColor(tip.priority)}`}>
                  Priority: {tip.priority}
                </span>
              </div>
              
              <div className="tip-content">
                <p>{tip.tip_text}</p>
              </div>
              
              <div className="tip-footer">
                <span className="tip-date">
                  {new Date(tip.created_at).toLocaleDateString()}
                </span>
                {!tip.is_read && (
                  <button 
                    className="mark-read-btn"
                    onClick={() => markAsRead(tip.id)}
                  >
                    ✓ Mark as Read
                  </button>
                )}
                {tip.is_read && (
                  <span className="read-badge">✓ Read</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="tips-info">
        <h3>About Your Health Tips</h3>
        <p>
          Our AI analyzes your health metrics and generates personalized recommendations 
          to help you achieve your wellness goals. Tips are prioritized based on urgency 
          and relevance to your current health status.
        </p>
      </div>
    </div>
  );
};

export default HealthTips;