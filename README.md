# Health Monitoring System

A comprehensive health tracking system with predictive analytics and AI-powered insights.

## Features

- 🔐 JWT Authentication
- 📊 Track 5 health metrics (weight, blood pressure, glucose, heart rate, steps)
- 🤖 Predictive analytics for weight trends
- 🩺 Diabetes risk assessment
- 🚨 Anomaly detection in health data
- 💡 AI-generated health tips
- 📈 Real-time health summaries with caching

## Tech Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT (Simple JWT)
- **Task Queue**: Celery

### Machine Learning
- scikit-learn
- pandas
- numpy

### Frontend (Coming Soon)
- React.js
- Chart.js for visualizations

### DevOps
- Docker & Docker Compose
- Gunicorn (Production server)

## Project Structure
```
health-monitoring-system/
├── backend/
│   ├── config/           # Django project settings
│   ├── users/            # User authentication app
│   ├── health_metrics/   # Health data tracking
│   ├── analytics/        # ML & predictive models
│   ├── ml_models/        # Trained model files
│   └── requirements.txt
├── frontend/             # React frontend (WIP)
├── docker/               # Docker configurations
└── docker-compose.yml
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- PostgreSQL 15
- Redis 7
- Docker (optional)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd health-monitoring-system
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Mac/Linux

pip install -r requirements.txt
```

3. **Environment Configuration**
Create `.env` file in backend directory:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=health_monitoring_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
```

4. **Database Setup**
```bash
# Using Docker
docker-compose up -d

# Or install PostgreSQL locally
```

5. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Start Development Server**
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## API Endpoints

### Authentication
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login (get JWT tokens)
- `POST /api/users/token/refresh/` - Refresh access token
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update profile

### Health Metrics
- `GET /api/health/metrics/` - List all metrics
- `POST /api/health/metrics/` - Create new metric entry
- `GET /api/health/metrics/{id}/` - Get specific metric
- `GET /api/health/summary/` - Get health summary (cached)
- `GET /api/health/anomalies/` - List active anomalies

### Analytics (Coming Soon)
- `GET /api/analytics/weight-prediction/` - Weight trend prediction
- `GET /api/analytics/diabetes-risk/` - Diabetes risk assessment
- `GET /api/analytics/health-tips/` - AI-generated tips

## Development Progress

- [x] Project setup & structure
- [x] User authentication (JWT)
- [x] Health metrics tracking
- [x] Database models & migrations
- [x] REST API endpoints
- [x] Redis caching
- [ ] ML models (weight prediction)
- [ ] Diabetes risk assessment
- [ ] Anomaly detection
- [ ] AI health tips
- [ ] Celery background tasks
- [ ] Frontend dashboard
- [ ] Docker containerization
- [ ] Production deployment



## License

MIT License

## Author

Your Name - [Shivanjali13]

---

**Status**: 🚧 Work in Progress - Phase 2 Complete (Steps 1-5)