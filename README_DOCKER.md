# 🐳 Docker Deployment Guide - PokeKawaii

This guide explains how to run the PokeKawaii game using Docker and Docker Compose.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: version 20.10 or higher
- **Docker Compose**: version 2.0 or higher

To check your installation:

```bash
docker --version
docker-compose --version
```

## 🏗️ Project Structure

```
PokeKawaii/
├── backend/
│   ├── Dockerfile              # Backend Docker configuration
│   ├── .dockerignore          # Files to exclude from backend image
│   ├── requirements.txt       # Python dependencies
│   └── app/                   # FastAPI application
├── frontend/
│   ├── Dockerfile             # Frontend Docker configuration (multi-stage)
│   ├── .dockerignore         # Files to exclude from frontend image
│   ├── nginx.conf            # Nginx configuration for production
│   ├── package.json          # Node.js dependencies
│   └── src/                  # React application
└── docker-compose.yml        # Orchestration configuration
```

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Clone the repository** (if not already done):
   ```bash
   cd /path/to/PokeKawaii
   ```

2. **Build and start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - **Frontend**: http://localhost
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

4. **Stop the application**:
   ```bash
   # Press Ctrl+C in the terminal, then:
   docker-compose down
   ```

### Option 2: Run in Detached Mode

Run containers in the background:

```bash
# Start services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Docker Commands

### Build Services

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend

# Build without cache (clean build)
docker-compose build --no-cache
```

### Start/Stop Services

```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

### View Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend

# View last 100 lines
docker-compose logs --tail=100
```

### Service Management

```bash
# List running containers
docker-compose ps

# Restart services
docker-compose restart

# Restart specific service
docker-compose restart backend

# Execute command in running container
docker-compose exec backend python -c "print('Hello')"
docker-compose exec frontend sh
```

### Health Check

```bash
# Check service health status
docker-compose ps

# View detailed health info
docker inspect pokekawaii-backend | grep -A 10 Health
docker inspect pokekawaii-frontend | grep -A 10 Health
```

## 🛠️ Development Mode

For development with hot-reload:

1. **Uncomment the volume mount** in `docker-compose.yml`:
   ```yaml
   backend:
     volumes:
       - ./backend/app:/app/app  # Enable hot-reload
   ```

2. **Rebuild and restart**:
   ```bash
   docker-compose up --build
   ```

Now changes to backend code will automatically reload the server.

> **Note**: Frontend uses nginx in production mode. For frontend development, use `npm run dev` locally instead.

## 🌐 Network Architecture

```
┌─────────────────┐
│   Browser       │
│  (localhost)    │
└────────┬────────┘
         │
         │ Port 80
         ▼
┌─────────────────────┐
│   Frontend          │
│   (Nginx)           │
│   pokekawaii-       │
│   frontend          │
└────────┬────────────┘
         │
         │ Proxy /api
         ▼
┌─────────────────────┐
│   Backend           │
│   (FastAPI)         │
│   pokekawaii-       │
│   backend           │
└─────────────────────┘
         │
         │ Port 8000
         ▼
  pokekawaii-network
    (Bridge)
```

## 📦 Service Details

### Backend Service

- **Image**: Python 3.11-slim
- **Port**: 8000
- **Framework**: FastAPI + Uvicorn
- **Health Check**: `/pokemon` endpoint
- **Restart Policy**: unless-stopped

### Frontend Service

- **Build Stage**: Node 20-alpine
- **Runtime Stage**: Nginx alpine
- **Port**: 80
- **Build Tool**: Vite
- **Health Check**: HTTP on port 80
- **Restart Policy**: unless-stopped

## 🔍 Troubleshooting

### Issue: Port Already in Use

```bash
# Check what's using port 80
sudo lsof -i :80

# Or use different port in docker-compose.yml
ports:
  - "8080:80"  # Map to port 8080 instead
```

### Issue: Backend Health Check Failing

```bash
# Check backend logs
docker-compose logs backend

# Test backend manually
docker-compose exec backend curl http://localhost:8000/pokemon
```

### Issue: Frontend Can't Connect to Backend

```bash
# Check network connectivity
docker-compose exec frontend ping backend

# Verify nginx config
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf
```

### Issue: Build Fails

```bash
# Clean everything and rebuild
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Issue: Out of Disk Space

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Clean everything (careful!)
docker system prune -a --volumes
```

## 🔐 Production Deployment

For production deployment, consider these improvements:

### 1. Environment Variables

Create a `.env` file:

```env
# .env
BACKEND_PORT=8000
FRONTEND_PORT=80
ENVIRONMENT=production
```

Update `docker-compose.yml`:

```yaml
backend:
  env_file:
    - .env
  environment:
    - ENVIRONMENT=${ENVIRONMENT}
```

### 2. Remove Development Volumes

Comment out or remove development volume mounts:

```yaml
backend:
  # volumes:
  #   - ./backend/app:/app/app  # Remove in production
```

### 3. Use Docker Secrets

For sensitive data:

```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  backend:
    secrets:
      - db_password
```

### 4. Add Reverse Proxy (Optional)

Use Traefik or Nginx as reverse proxy:

```yaml
services:
  traefik:
    image: traefik:v2.10
    # ... configuration
```

### 5. Enable SSL/TLS

Add Let's Encrypt with Certbot or use Traefik's ACME.

## 📊 Resource Limits

Add resource constraints for production:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## 🧪 Testing the Deployment

### Test Backend

```bash
# Test API endpoint
curl http://localhost:8000/pokemon

# Test new game creation
curl -X POST http://localhost:8000/api/game/new
```

### Test Frontend

```bash
# Test homepage
curl http://localhost

# Check if assets are served
curl http://localhost/assets/
```

## 📈 Monitoring

### View Resource Usage

```bash
# Real-time stats
docker stats

# Specific container
docker stats pokekawaii-backend
```

### Export Logs

```bash
# Export to file
docker-compose logs > logs.txt

# Export with timestamp
docker-compose logs -t > logs_$(date +%Y%m%d_%H%M%S).txt
```

## 🔄 Updating the Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose up --build -d

# Or use rolling update
docker-compose up -d --build --no-deps backend
```

## 🧹 Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove everything (containers, networks, volumes, images)
docker-compose down -v --rmi all

# Clean Docker system
docker system prune -a --volumes
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)
- [Nginx Docker Guide](https://hub.docker.com/_/nginx)

## 🆘 Getting Help

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify health: `docker-compose ps`
3. Test connectivity: `docker-compose exec backend ping frontend`
4. Rebuild from scratch: `docker-compose down -v && docker-compose up --build`

## 📝 Notes

- **Development**: Backend supports hot-reload when volume is mounted
- **Production**: Frontend is built as static files served by Nginx
- **API Proxy**: Nginx proxies `/api` requests to backend automatically
- **Health Checks**: Both services have health checks configured
- **Network**: Services communicate via internal Docker network

---

**Enjoy playing PokeKawaii! 🎮✨**
