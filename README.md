# SEO Content Agent with Masumi Integration

A sophisticated AI-powered SEO content generation agent integrated with Masumi for decentralized payments and agent identity management.

## Features

- **SEO Content Generation**: Automatically generate SEO-optimized blog posts and landing pages
- **Keyword Research**: Analyze keywords and generate relevant keyword suggestions
- **SEO Analysis**: Comprehensive content optimization analysis with actionable recommendations
- **Masumi Integration**: Decentralized payment handling and agent identity management
- **Payment Processing**: Create, confirm, and manage payments through Masumi
- **Webhook Support**: Handle payment confirmation webhooks from Masumi
- **FastAPI Server**: RESTful API for content generation and payment management
- **Docker Support**: Container-based deployment with Docker Compose

## Project Structure

```
seo-content-agent/
├── agent/                          # Core SEO content logic
│   ├── main.py                    # Entry point and orchestrator
│   ├── content_generator.py       # Content generation templates
│   ├── keyword_research.py        # Keyword analysis tools
│   ├── seo_analyzer.py           # SEO optimization analysis
│   └── templates/                # Content templates
│
├── masumi-integration/            # Payment and identity management
│   ├── payment_client.py         # Masumi payment API client
│   ├── identity_manager.py       # Agent identity management
│   └── webhook_handler.py        # Payment webhook handling
│
├── api/                          # FastAPI REST endpoints
│   ├── server.py                 # API server
│   └── routes.py                 # Route handlers
│
├── tests/                        # Unit tests
│   ├── test_content.py          # Content generation tests
│   └── test_payments.py         # Payment integration tests
│
├── requirements.txt             # Python dependencies
├── docker-compose.yml          # Docker services configuration
├── Dockerfile                  # Docker image definition
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Installation

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional)
- Masumi API key

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/seo-content-agent.git
cd seo-content-agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your Masumi API key and other settings
```

5. **Run the server**
```bash
python -m api.server
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

2. **Build and start services**
```bash
docker-compose up -d
```

3. **View logs**
```bash
docker-compose logs -f seo-agent-api
```

## Usage

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Generate SEO Content
```bash
curl -X POST http://localhost:8000/api/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Sustainable Web Hosting",
    "content_type": "blog_post",
    "target_keywords": ["sustainable hosting", "green web"]
  }'
```

#### Research Keywords
```bash
curl "http://localhost:8000/api/keyword-research?topic=Web%20Development&limit=5"
```

#### Analyze Content for SEO
```bash
curl -X GET "http://localhost:8000/api/seo-analysis?title=My%20Title&description=My%20Description&body=My%20content"
```

#### Create Payment
```bash
curl -X POST http://localhost:8000/api/payments/create \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5.00,
    "description": "Content generation service",
    "agent_id": "agent_001"
  }'
```

#### Register Agent
```bash
curl -X POST "http://localhost:8000/api/agents/register?agent_name=MyAgent"
```

#### Get Agent Info
```bash
curl http://localhost:8000/api/agents/{agent_id}
```

## Running Tests

```bash
pytest tests/ -v
pytest tests/ --cov=agent --cov=masumi_integration --cov=api
```

## Configuration

### Environment Variables

See `.env.example` for all available configuration options:

- `MASUMI_API_KEY`: Your Masumi API key
- `MASUMI_BASE_URL`: Masumi API endpoint
- `WEBHOOK_SECRET`: Secret for webhook signature verification
- `API_HOST`: Server host (default: 0.0.0.0)
- `API_PORT`: Server port (default: 8000)
- `CORS_ORIGINS`: Allowed CORS origins
- `LOG_LEVEL`: Logging level (default: INFO)

## Architecture

### Agent Component
- **ContentGenerator**: Generates content from templates with keyword optimization
- **KeywordResearcher**: Analyzes and suggests relevant keywords
- **SEOAnalyzer**: Evaluates content quality and provides optimization tips

### Masumi Integration
- **MasumiPaymentClient**: Handles payment creation and confirmation
- **AgentIdentity**: Manages agent credentials and Masumi wallet
- **WebhookHandler**: Processes payment confirmation webhooks

### API Layer
- FastAPI-based REST API
- Async request handling
- CORS support
- Built-in health checks

## Development

### Code Style
```bash
black .
flake8 .
isort .
```

### Type Checking
```bash
mypy agent masumi_integration api
```

## Performance Considerations

- Content generation is cached based on topic and keywords
- Keyword research results are memoized
- Payment transactions are idempotent
- Webhook events prevent duplicate processing

## Security

- Webhook signature verification
- Environment variable-based configuration
- No secrets in version control
- CORS restrictions
- Input validation on all endpoints

## Deployment

### Production Deployment

```bash
# Using Docker
docker build -t seo-agent:latest .
docker run -p 8000:8000 --env-file .env seo-agent:latest

# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 api.server:app
```

### Scaling

- Use Docker Swarm or Kubernetes for container orchestration
- Load balance multiple API instances
- Use PostgreSQL for persistent storage
- Configure Masumi webhook endpoints for all instances

## Monitoring and Logging

- JSON structured logs for easy parsing
- Request/response logging on API endpoints
- Payment transaction audit trail
- Webhook event logging for compliance

## Troubleshooting

### Payment Creation Fails
- Verify `MASUMI_API_KEY` is set correctly
- Check Masumi service connectivity
- Review logs for specific error messages

### Content Generation Issues
- Ensure template files are present in `agent/templates/`
- Verify keyword research API connectivity
- Check available system memory

### Webhook Processing
- Verify webhook signature is correct
- Check webhook secret in `.env`
- Review webhook event logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Email: support@seo-agent.dev
- Documentation: https://docs.seo-agent.dev

## Roadmap

- [ ] Multi-language content generation
- [ ] Advanced SEO recommendations engine
- [ ] Content performance analytics
- [ ] Integration with search engines
- [ ] Real-time collaboration features
- [ ] Mobile app support
