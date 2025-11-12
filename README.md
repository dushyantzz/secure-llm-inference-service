# Secure LLM Inference Service

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready FastAPI service for secure, fast local LLM inference using Ollama and Gemma models. Features JWT authentication, rate limiting, structured logging, and comprehensive performance monitoring.

## 🎯 Features

- **🔒 Secure Authentication**: JWT token-based authentication with bcrypt password hashing
- **⚡ Fast Inference**: Optimized for low-latency responses using Gemma 2B model
- **🚦 Rate Limiting**: Configurable rate limiting (default: 10 requests/minute per user)
- **📊 Performance Monitoring**: Real-time metrics tracking (average latency, P95, request counts)
- **📝 Structured Logging**: JSON-formatted logs with request details and performance data
- **🐳 Docker Support**: Complete containerization with Docker and docker-compose
- **🏥 Health Checks**: Built-in health endpoints for monitoring service status

## 📋 Requirements

- Python 3.11+
- [Ollama](https://ollama.ai/) installed and running
- 4GB+ RAM (for Gemma 2B model)
- GPU (optional, GTX 1650 or better recommended)

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/dushyantzz/secure-llm-inference-service.git
cd secure-llm-inference-service

# Run setup script
chmod +x setup.sh
./setup.sh

# Start the server
source venv/bin/activate
uvicorn app.main:app --reload
```

### Option 2: Manual Setup

```bash
# 1. Install and start Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve

# 2. Pull Gemma model
ollama pull gemma:2b

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env with your settings (especially JWT_SECRET_KEY)

# 6. Start the server
uvicorn app.main:app --reload
```

### Option 3: Docker Deployment

```bash
# Start with docker-compose
docker-compose up -d

# Pull Gemma model in Ollama container
docker-compose exec ollama ollama pull gemma:2b

# Check logs
docker-compose logs -f api
```

## 🔑 Authentication

### Default Credentials
- **Username**: `demo`
- **Password**: `demo1234`

### Get Access Token

```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=demo1234"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## 📡 API Endpoints

### 1. Inference Endpoint

**POST** `/v1/infer`

Generate responses from the local LLM.

```bash
curl -X POST "http://localhost:8000/v1/infer" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a haiku about fast inference."}'
```

**Response:**
```json
{
  "response": "Thoughts form in silence,\nBits race through neural pathways,\nAnswers bloom swiftly."
}
```

### 2. Metrics Endpoint

**GET** `/metrics`

Get performance metrics (requires authentication).

```bash
curl -X GET "http://localhost:8000/metrics" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**
```json
{
  "total_requests": 42,
  "successful_requests": 40,
  "failed_requests": 2,
  "average_latency_ms": 245.67,
  "p95_latency_ms": 312.45,
  "uptime_seconds": 3600
}
```

### 3. Health Check

**GET** `/health`

Check service and Ollama status.

```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "ollama_service": "up",
  "model": "gemma:2b"
}
```

## 🧪 Testing

Run the automated test suite:

```bash
chmod +x test_api.sh
./test_api.sh
```

This will test:
- Health check
- Authentication
- Inference endpoint
- Metrics collection
- Rate limiting

## ⚙️ Configuration

Edit `.env` file to customize settings:

```env
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma:2b

# Rate Limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60

# API Configuration
API_VERSION=v1
LOG_LEVEL=INFO
```

## 📊 Performance Optimization

### Latency Targets
- **API Overhead**: < 300ms (excluding LLM inference)
- **Total Response Time**: Varies by prompt complexity
- **Rate Limit**: 10 requests/minute per user (configurable)

### Tips for Better Performance
1. Use smaller models for faster responses (gemma:2b recommended for GTX 1650)
2. Keep prompts concise
3. Enable GPU acceleration in Ollama
4. Increase rate limits for production use
5. Monitor metrics endpoint for performance insights

## 📝 Logging

All requests are logged in structured JSON format:

```json
{
  "timestamp": "2025-11-12T17:30:45.123456",
  "level": "INFO",
  "message": "Inference completed successfully",
  "module": "main",
  "user_id": "demo",
  "prompt_length": 45,
  "response_length": 127,
  "latency_ms": 234.56,
  "status": "success"
}
```

## 🏗️ Project Structure

```
secure-llm-inference-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── auth.py              # JWT authentication
│   ├── rate_limiter.py      # Rate limiting middleware
│   ├── llm_service.py       # Ollama integration
│   ├── metrics.py           # Performance tracking
│   └── logging_config.py    # Structured logging
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── setup.sh                 # Automated setup script
├── test_api.sh             # API testing script
└── README.md
```

## 🔒 Security Considerations

1. **Change Default Credentials**: Update the demo user credentials in `app/auth.py`
2. **Secure JWT Secret**: Generate a strong secret key:
   ```bash
   openssl rand -hex 32
   ```
3. **HTTPS in Production**: Use reverse proxy (nginx) with SSL/TLS
4. **Database for Users**: Replace `fake_users_db` with a real database
5. **Environment Variables**: Never commit `.env` file to version control

## 🐛 Troubleshooting

### Ollama Connection Error
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

### Model Not Found
```bash
# Pull the Gemma model
ollama pull gemma:2b

# List installed models
ollama list
```

### Rate Limit Issues
- Adjust `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW` in `.env`
- Wait 60 seconds between test batches

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Dushyant**
- GitHub: [@dushyantzz](https://github.com/dushyantzz)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Google Gemma](https://ai.google.dev/gemma) - Lightweight LLM

---

**Note**: This service is designed for local development and testing. For production deployment, consider additional security measures, database integration, and horizontal scaling.
