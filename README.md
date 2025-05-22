# Recipe Extractor API

A FastAPI endpoint that extracts structured recipe data from any recipe URL using AI. Built with the Instructor library for reliable structured outputs from LLMs.

## Features

- 🔗 Extract recipes from any URL
- 📝 Structured JSON output with ingredients, steps, and metadata
- 🖼️ Extracts recipe images
- ⏱️ Cooking times and servings information
- 🏷️ Recipe tags and categories
- 🥗 Nutritional information (when available)
- 🚀 Ready for production deployment

## Setup

### Prerequisites

- Python 3.11+
- OpenAI API key
- uv (for package management)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/victoriano/recipepe.git
cd recipepe
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Create a `.env` file with your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
```

### Running Locally

```bash
uv run python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

### Endpoints

#### `POST /extract`

Extract recipe data from a URL.

**Request Body:**
```json
{
  "url": "https://example.com/recipe-page"
}
```

**Response:**
```json
{
  "success": true,
  "recipe": {
    "title": "Chocolate Chip Cookies",
    "description": "Classic homemade chocolate chip cookies",
    "prep_time": "15 minutes",
    "cook_time": "12 minutes",
    "total_time": "27 minutes",
    "servings": "24 cookies",
    "difficulty": "Easy",
    "cuisine": "American",
    "course": "Dessert",
    "ingredients": [
      {
        "name": "all-purpose flour",
        "amount": "2 1/4",
        "unit": "cups",
        "notes": null
      }
    ],
    "steps": [
      {
        "step_number": 1,
        "instruction": "Preheat oven to 375°F",
        "duration": null
      }
    ],
    "image_urls": ["https://example.com/cookie-image.jpg"],
    "nutrition_info": {"calories": "150"},
    "tags": ["cookies", "dessert", "baking"],
    "author": "Recipe Author",
    "source_url": "https://example.com/recipe-page"
  }
}
```

#### `GET /health`

Health check endpoint.

## Deployment Options

### 🚀 Automated GitHub Deployment (Recommended)

The easiest way to deploy with full CI/CD:

```bash
./setup-github-deployment.sh
```

This will:
- ✅ Create GitHub repository
- ✅ Configure deployment secrets
- ✅ Set up automated deployment to Hetzner
- ✅ Enable deployment on every push to main

### 🟢 Hetzner Server

Perfect for Python applications! Full Docker support with excellent performance.

#### Quick Hetzner Deployment

1. **Get a Hetzner VPS:**
   - Sign up at [Hetzner Cloud](https://www.hetzner.com/cloud)
   - Create a new VPS (CX11 is sufficient to start - €3.29/month)
   - Note your server IP

2. **Deploy:**
   ```bash
   ./deploy.sh
   ```

### 🔵 Other Options

#### Railway (Easiest)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### Fly.io
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
flyctl deploy
```

## Cost Estimates

### Server Hosting
- **Hetzner CX11**: €3.29/month (1 vCPU, 2GB RAM)
- **Railway**: $5/month (512MB RAM)
- **Fly.io**: ~$5/month

### API Usage
- **OpenAI GPT-4o-mini**: ~$0.01-0.05 per recipe extraction
- For 1000 recipes/month: ~$10-50 in API costs

## Development

### Local Testing

```bash
# Test deployment locally
./test-local-deployment.sh

# Run tests
uv run python test_api.py
```

### Making Changes

1. Make your changes locally
2. Test with `./test-local-deployment.sh`
3. Commit and push - automatic deployment will trigger

```bash
git add .
git commit -m "feat: your changes"
git push
```

## Docker

### Local Development

```bash
# Build and run
docker-compose up --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production

The Docker setup includes:
- FastAPI application with health checks
- Nginx reverse proxy with rate limiting
- Automatic container restart on failure
- SSL/HTTPS support (with certificate setup)

## Features

### Supported Recipe Sources
- Works with most recipe websites
- Handles multiple languages
- Extracts structured data including:
  - Ingredients with amounts and units
  - Step-by-step instructions
  - Cooking times and servings
  - Recipe images
  - Nutritional information
  - Tags and categories

### AI-Powered Extraction
- Uses OpenAI GPT-4o-mini for cost-effective extraction
- Instructor library ensures reliable structured outputs
- Automatic retry logic for robustness
- Handles various website formats and layouts

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test locally
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the [GitHub Issues](https://github.com/victoriano/recipepe/issues)
2. Review the deployment logs if using automated deployment
3. Test locally with the provided test scripts

---

🚀 **Ready to extract recipes at scale!** Start with the automated deployment for the best experience.