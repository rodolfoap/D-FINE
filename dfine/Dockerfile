ARG BASE_IMAGE_VERSION=8.1.1
FROM registry.gtd-international.com/me_ia/infrastructure/base-images/base_cuda:${BASE_IMAGE_VERSION}

# Install system dependencies
RUN apt-get update && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies using BuildKit secret for PyPI token
# Build with: docker buildx build --secret gitlab_token=<token> ...
COPY requirements.txt .
RUN rm /usr/lib/python3.12/EXTERNALLY-MANAGED
RUN --mount=type=secret,id=gitlab_token \
    pip3 install -r requirements.txt \
    --extra-index-url "https://oauth2:$(cat /run/secrets/gitlab_token)@git.gtd-international.com/api/v4/packages/pypi/simple" \
    2>/dev/null

# Copy D-FINE source code
COPY . .

# Small bugfix
RUN groupadd -g 105 inference

# Set PYTHONPATH for imports
ENV PYTHONPATH="/app"

# Run detection module
ENTRYPOINT ["python3", "detection.py"]
