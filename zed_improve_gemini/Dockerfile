FROM modular/mojo:latest

# Install basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Create application user and directories
RUN useradd -m -u 1000 -s /bin/bash gemini_user

# Create required directories
RUN mkdir -p /app/data /app/logs /app/cache /tmp/gemini_api && \
    chown -R gemini_user:gemini_user /app /tmp/gemini_api

# Copy initialization and testing scripts
COPY init-directories.sh /usr/local/bin/
COPY test-writable-dirs.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/*.sh

# Copy Mojo application
COPY GeminiAPIHandler.mojo /app/
COPY *.mojo /app/

# Set working directory
WORKDIR /app

# Switch to application user
USER gemini_user

# Set environment variables
ENV REQUIRED_DIRS="/app/data /app/logs /app/cache /tmp/gemini_api"
ENV DEFAULT_PERMS="755"
ENV WRITABLE_DIRS="/app/data /app/logs /app/cache /tmp/gemini_api"

# Use init script as entrypoint
ENTRYPOINT ["/usr/local/bin/init-directories.sh"]

# Default command
CMD ["mojo", "run", "GeminiAPIHandler.mojo"]