FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG GO_VERSION=1.26.3
ARG NODE_MAJOR=22

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl unzip ca-certificates \
    && curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && curl -fsSL "https://go.dev/dl/go${GO_VERSION}.linux-$(dpkg --print-architecture).tar.gz" -o /tmp/go.tar.gz \
    && tar -C /usr/local -xzf /tmp/go.tar.gz \
    && rm /tmp/go.tar.gz \
    && curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m).zip" -o /tmp/awscliv2.zip \
    && unzip -q /tmp/awscliv2.zip -d /tmp \
    && /tmp/aws/install \
    && rm -rf /tmp/awscliv2.zip /tmp/aws \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/go/bin:/home/vscode/go/bin:${PATH}"
