# AI381 Lab 2 — Containerised Churn API

[![ci](https://github.com/YOURUSERNAME/ai381-lab2/actions/workflows/ci.yml/badge.svg)](https://github.com/YOURUSERNAME/ai381-lab2/actions/workflows/ci.yml)

A FastAPI service that serves the churn model from Lab 1. Multi-stage Dockerfile,
non-root container, HEALTHCHECK, and CI via GitHub Actions that scans with Trivy
and pushes to GHCR tagged with the commit SHA.

## One-command start

```bash
docker run -p 8000:8000 ghcr.io/YOURUSERNAME/ai381-lab2:<sha>Lab 2 — containerised churn API with CI
