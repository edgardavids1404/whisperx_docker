# Base image with CUDA + cuDNN support
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

# Set non-interactive frontend for apt to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
        apt-get install -y python3 python3-pip && \
        apt-get install -y supervisor && \
        apt-get install -y ffmpeg && \
	apt-get install -y curl && \
	apt-get install -y git-lfs && \
	git lfs intall && \
        rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

RUN python3 download_models.py

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports for FastAPI and Streamlit
EXPOSE 8501 8502

# Default command
CMD ["/usr/bin/supervisord"]
