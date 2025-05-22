# 🚀 Deployment Guide

This guide will help you set up automatic deployment to your Hetzner server using GitHub Actions.

## 📋 Prerequisites

1. **Hetzner VPS** - Any size will work (CX11 recommended for testing)
2. **GitHub Account** - For hosting the repository
3. **GitHub CLI** - For easy setup (will be installed automatically on macOS)
4. **OpenAI API Key** - For the recipe extraction functionality

## 🎯 Quick Setup (Automated)

The easiest way to set everything up:

```bash
./setup-github-deployment.sh
```

This script will:
- ✅ Install GitHub CLI (if needed)
- ✅ Create a public GitHub repository
- ✅ Configure deployment secrets
- ✅ Set up SSH access to your server
- ✅ Push your code to GitHub
- ✅ Trigger the first deployment

## 🔧 Manual Setup

If you prefer to set things up manually:

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Make it public
3. Don't initialize with README (we already have one)

### Step 2: Add Your Repository as Remote

```bash
git remote add origin https://github.com/yourusername/your-repo-name.git
```

### Step 3: Configure GitHub Secrets

Go to your repository settings → Secrets and variables → Actions, and add:

- `HETZNER_SERVER_IP`: Your Hetzner server's IP address
- `HETZNER_SSH_KEY`: Your SSH private key for accessing the server

### Step 4: Set Up SSH Access

If you don't have SSH access to your server yet:

1. Generate SSH key (if you don't have one):
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
   ```

2. Copy your public key to the server:
   ```bash
   ssh-copy-id root@your-server-ip
   ```

### Step 5: Push Your Code

```bash
git add .
git commit -m "feat: initial commit - Recipe Extractor API"
git branch -M main
git push -u origin main
```

## 🤖 How Automated Deployment Works

When you push to the `main` branch, GitHub Actions will:

1. **Test Phase:**
   - ✅ Install dependencies with `uv`
   - ✅ Run basic import tests
   - ✅ Validate code structure

2. **Deploy Phase:**
   - 📦 Create deployment package
   - 🔑 Set up SSH connection to your server
   - 📤 Copy files to server
   - 🐳 Install Docker (if needed)
   - 🔨 Build and start containers
   - 🧪 Run health checks
   - ✅ Confirm deployment success

## 📊 Monitoring Your Deployment

### Check Deployment Status

```bash
# View recent deployments
gh run list

# View specific deployment logs
gh run view [run-id]
```

### Monitor Your Server

```bash
# SSH into your server
ssh root@your-server-ip

# Check container status
cd /opt/recipepe
docker-compose ps

# View application logs
docker-compose logs -f

# Restart containers
docker-compose restart
```

### Test Your API

```bash
# Health check
curl http://your-server-ip:8000/health

# Test recipe extraction
curl -X POST http://your-server-ip:8000/extract \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/"}'
```

## 🔒 Security Configuration

### Environment Variables

The deployment automatically creates a `.env` file on your server. You need to add your OpenAI API key:

```bash
ssh root@your-server-ip
echo "OPENAI_API_KEY=your-openai-api-key-here" > /opt/recipepe/.env
cd /opt/recipepe
docker-compose restart
```

### SSL/HTTPS Setup (Optional)

To enable HTTPS:

1. Get SSL certificates (Let's Encrypt recommended):
   ```bash
   # On your server
   apt install certbot
   certbot certonly --standalone -d your-domain.com
   ```

2. Update nginx configuration:
   ```bash
   # Uncomment SSL lines in nginx.conf
   # Copy certificates to ssl/ directory
   ```

3. Restart nginx:
   ```bash
   docker-compose restart nginx
   ```

## 🚀 Development Workflow

### Making Changes

1. **Local Development:**
   ```bash
   # Test locally first
   ./test-local-deployment.sh
   ```

2. **Push Changes:**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   git push
   ```

3. **Automatic Deployment:**
   - GitHub Actions will automatically test and deploy
   - Check the Actions tab on GitHub for status
   - Your changes will be live in ~3-5 minutes

### Rollback Strategy

If a deployment fails:

1. **Automatic Rollback:**
   - The deployment script backs up previous versions
   - Failed deployments won't affect running containers

2. **Manual Rollback:**
   ```bash
   ssh root@your-server-ip
   cd /opt/recipepe
   
   # View backups
   ls backup/
   
   # Restore from backup
   cp -r backup/YYYYMMDD_HHMMSS/* .
   docker-compose up -d --build
   ```

## 📈 Scaling Considerations

### Performance Monitoring

Monitor these metrics:
- Response times (`curl -w "Total time: %{time_total}s\n"`)
- Memory usage (`docker stats`)
- OpenAI API usage (OpenAI dashboard)

### Scaling Options

1. **Vertical Scaling:**
   - Upgrade your Hetzner VPS
   - Increase container resources in docker-compose.yml

2. **Load Balancing:**
   - Add multiple replicas in docker-compose.yml
   - Use nginx load balancing

3. **Caching:**
   - Add Redis for response caching
   - Implement request deduplication

## 🔧 Troubleshooting

### Common Issues

1. **Deployment Fails:**
   ```bash
   # Check GitHub Actions logs
   gh run view --log
   
   # SSH to server and check
   ssh root@your-server-ip 'cd /opt/recipepe && docker-compose logs'
   ```

2. **Container Won't Start:**
   ```bash
   # Check Docker status
   ssh root@your-server-ip 'systemctl status docker'
   
   # Check container logs
   ssh root@your-server-ip 'cd /opt/recipepe && docker-compose logs recipepe'
   ```

3. **API Errors:**
   ```bash
   # Check OpenAI API key
   ssh root@your-server-ip 'cd /opt/recipepe && cat .env'
   
   # Test API key
   curl -H "Authorization: Bearer your-api-key" https://api.openai.com/v1/models
   ```

### Health Checks

The deployment includes automatic health checks:
- Container health checks every 30 seconds
- Deployment verification with retry logic
- Automatic container restart on failure

## 💰 Cost Optimization

### Server Costs
- **Hetzner CX11**: €3.29/month (1 vCPU, 2GB RAM) - sufficient for moderate traffic
- **Hetzner CX21**: €5.83/month (2 vCPU, 4GB RAM) - better for higher traffic

### API Costs
- **OpenAI GPT-4o-mini**: ~$0.01-0.05 per recipe extraction
- Monitor usage at [OpenAI Usage Dashboard](https://platform.openai.com/usage)
- Set up billing alerts to avoid surprises

## 📞 Support

If you run into issues:

1. Check the [GitHub Actions logs](https://github.com/your-username/your-repo/actions)
2. Review server logs: `ssh root@your-server-ip 'cd /opt/recipepe && docker-compose logs'`
3. Test locally with `./test-local-deployment.sh`
4. Check the [troubleshooting section](#troubleshooting) above

## 🎉 Success!

Once everything is set up, you'll have:
- ✅ Automatic deployments on every push
- ✅ Professional CI/CD pipeline
- ✅ Scalable Docker deployment
- ✅ Health monitoring and automatic restarts
- ✅ Backup and rollback capabilities

Your API will be available at: `http://your-server-ip:8000` 