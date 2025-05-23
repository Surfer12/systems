# Gemini API Handler with Environment Integration

A robust Mojo-based API handler for Google's Gemini API that includes comprehensive error handling, rate limiting, and environment validation.

## 🚀 Features

- **Rate Limit Handling**: Exponential backoff with jitter for API rate limits
- **Environment Validation**: Comprehensive directory permission testing
- **Container Ready**: Docker and Kubernetes deployment configurations
- **Monitoring**: Usage metrics and diagnostic reporting
- **Fault Tolerance**: Graceful error recovery and user communication
- **Multi-Scale Architecture**: Works across development, staging, and production

## 📁 Project Structure

```
zed_improve_gemini/
├── GeminiAPIHandler.mojo          # Main Mojo implementation
├── init-directories.sh            # Directory initialization script
├── test-writable-dirs.sh          # Permission testing script
├── environment_diagnostics.py     # Comprehensive diagnostics
├── Dockerfile                     # Container build configuration
├── docker-compose.yml             # Local development setup
├── k8s-deployment.yaml            # Kubernetes deployment
└── README.md                      # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- [Mojo](https://www.modular.com/mojo) runtime
- Python 3.8+ (for diagnostics)
- Docker (for containerized deployment)
- Kubernetes (for cluster deployment)

### Local Development

1. **Clone and Navigate**:
   ```bash
   cd /Users/ryandavidoates/systems/zed_improve_gemini
   ```

2. **Set Environment Variables**:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   export REQUIRED_DIRS="/app/data /app/logs /app/cache /tmp/gemini_api"
   ```

3. **Initialize Environment**:
   ```bash
   chmod +x *.sh
   ./init-directories.sh
   ```

4. **Run Diagnostics**:
   ```bash
   python3 environment_diagnostics.py
   ```

5. **Test the Handler**:
   ```bash
   mojo run GeminiAPIHandler.mojo
   ```

### Docker Deployment

1. **Build the Image**:
   ```bash
   docker build -t gemini-api-handler .
   ```

2. **Run with Docker Compose**:
   ```bash
   # Create required host directories
   mkdir -p data logs
   
   # Set your API key
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   
   # Start the service
   docker-compose up -d
   ```

3. **Check Health**:
   ```bash
   docker-compose exec gemini-api-handler /usr/local/bin/test-writable-dirs.sh
   ```

### Kubernetes Deployment

1. **Create Namespace and Secret**:
   ```bash
   kubectl apply -f k8s-deployment.yaml
   
   # Set your API key
   kubectl create secret generic gemini-api-secret \
     --from-literal=api-key="your_api_key_here" \
     -n gemini-api
   ```

2. **Deploy Application**:
   ```bash
   kubectl apply -f k8s-deployment.yaml
   ```

3. **Check Status**:
   ```bash
   kubectl get pods -n gemini-api
   kubectl logs -f deployment/gemini-api-handler -n gemini-api
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Your Gemini API key | Required |
| `REQUIRED_DIRS` | Space-separated list of required directories | `/app/data /app/logs /app/cache /tmp/gemini_api` |
| `MAX_RETRIES` | Maximum retry attempts for rate limits | `5` |
| `BASE_RETRY_DELAY` | Base delay for exponential backoff (seconds) | `15.0` |
| `DEFAULT_PERMS` | Default directory permissions | `755` |

### Directory Structure

The handler requires these directories to be writable:

- `/app/data` - Application data storage
- `/app/logs` - Log file storage  
- `/app/cache` - Temporary cache files
- `/tmp/gemini_api` - Temporary processing files

## 🚨 Error Handling

### Rate Limit Errors (429)

When a rate limit is encountered, the handler:

1. **Identifies the Error**: Parses the 429 response from Gemini API
2. **Calculates Backoff**: Uses exponential backoff with jitter
3. **Provides Information**: Shows detailed error information and solutions
4. **Retries Automatically**: Implements up to 5 retry attempts
5. **Logs Metrics**: Tracks rate limit occurrences for analysis

### Example Rate Limit Response

```
🚨 RATE LIMIT ERROR ENCOUNTERED
============================================================
I've encountered a rate limit error (429). This means we've
exceeded the current API quota.

📊 Error Details:
  • Status: RESOURCE_EXHAUSTED
  • Quota Metric: generate_content_paid_tier_input_token_count
  • Current Limit: 2000000 tokens/minute
  • Model Affected: gemini-2.5-pro-exp
  • Suggested Retry Delay: 15s

🔧 Possible Solutions:
  1. Wait for the retry period (15 seconds)
  2. Upgrade your quota tier:
     → https://aistudio.google.com/apikey
  3. Submit a quota increase request:
     → https://ai.google.dev/gemini-api/docs/rate-limits#request-rate-limit-increase
  4. Implement request batching/optimization
  5. Use caching for repeated queries

🛡️ Prevention Strategies:
  • Monitor usage metrics regularly
  • Implement request prioritization
  • Use smaller batch sizes
  • Cache frequent requests
  • Distribute load across time
```

## 🔍 Diagnostics

### Running Diagnostics

```bash
# Basic diagnostics
python3 environment_diagnostics.py

# Quiet mode (warnings/errors only)
python3 environment_diagnostics.py --quiet

# Save report to custom file
python3 environment_diagnostics.py --output my_report.json

# Use custom configuration
python3 environment_diagnostics.py --config my_config.json
```

### Diagnostic Report Sections

1. **System Information**: Platform, Python version, user context
2. **Directory Permissions**: Read/write/execute access for all required directories
3. **API Configuration**: API key presence and format validation
4. **Runtime Environment**: Mojo availability, package dependencies
5. **Network Connectivity**: Endpoint reachability tests
6. **Performance Metrics**: Memory, CPU, disk I/O benchmarks

## 📊 Monitoring & Logging

### Usage Metrics

The handler automatically tracks:

- Total API requests
- Token consumption
- Error rates
- Rate limit hits
- Success rates
- Response times

### Log Files

Logs are written to `/app/logs/` and include:

- API usage events
- Rate limit encounters
- Environment initialization
- Error details
- Performance metrics

### Health Checks

Available health check endpoints:

- **Docker**: `docker-compose exec gemini-api-handler /usr/local/bin/test-writable-dirs.sh`
- **Kubernetes**: Automatic liveness/readiness probes
- **Manual**: `./test-writable-dirs.sh`

## 🔄 Development Workflow

### Local Testing

1. **Environment Setup**:
   ```bash
   ./init-directories.sh
   python3 environment_diagnostics.py
   ```

2. **Run Tests**:
   ```bash
   ./test-writable-dirs.sh
   mojo run GeminiAPIHandler.mojo
   ```

3. **Check Logs**:
   ```bash
   tail -f /app/logs/*.log
   ```

### Container Testing

1. **Build and Test**:
   ```bash
   docker build -t gemini-api-handler:test .
   docker run --rm -e GEMINI_API_KEY="test_key" gemini-api-handler:test
   ```

2. **Volume Testing**:
   ```bash
   docker run --rm -v $(pwd)/test_data:/app/data gemini-api-handler:test
   ```

## 🛡️ Security Considerations

### API Key Management

- **Environment Variables**: Store API keys in environment variables, never in code
- **Kubernetes Secrets**: Use proper secret management in Kubernetes
- **Docker Secrets**: Use Docker secrets for production deployments
- **Rotation**: Implement regular API key rotation

### Container Security

- **Non-root User**: Containers run as non-root user (UID 1000)
- **Read-only Filesystem**: Where possible, use read-only root filesystem
- **Resource Limits**: CPU and memory limits enforced
- **Security Context**: Proper security context in Kubernetes

### Network Security

- **TLS**: All API communications use HTTPS/TLS
- **Firewall**: Restrict outbound connections to required endpoints only
- **Network Policies**: Use Kubernetes network policies in production

## 🚀 Production Deployment

### Scaling Considerations

- **Horizontal Scaling**: Use Kubernetes HPA for automatic scaling
- **Rate Limiting**: Coordinate rate limits across multiple instances
- **Load Balancing**: Distribute requests evenly
- **Circuit Breakers**: Implement circuit breaker patterns

### Monitoring Setup

1. **Metrics Collection**: Set up Prometheus/Grafana
2. **Log Aggregation**: Use ELK stack or similar
3. **Alerting**: Configure alerts for rate limit hits, errors
4. **Dashboards**: Create operational dashboards

### Backup & Recovery

- **Configuration Backup**: Regular backup of configuration
- **Data Persistence**: Ensure data directories are properly backed up
- **Disaster Recovery**: Document recovery procedures

## 🤝 Contributing

1. **Code Style**: Follow Mojo and Python best practices
2. **Testing**: Add tests for new features
3. **Documentation**: Update README for changes
4. **Error Handling**: Ensure robust error handling

## 📚 References

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Mojo Programming Language](https://www.modular.com/mojo)
- [Rate Limiting Best Practices](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Security](https://kubernetes.io/docs/concepts/security/)

## 📄 License

This project is part of the systems research repository and follows the same licensing terms.

---

**Note**: This implementation demonstrates fractal communication principles by operating at multiple scales (micro: code structure, meso: container deployment, macro: cluster orchestration) while maintaining coherent patterns across all levels.