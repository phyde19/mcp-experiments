FROM python:3.11-bullseye

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    vim \
    curl \
    git \
    jq \
    procps \
    && apt clean && rm -rf /var/lib/apt/lists/*
