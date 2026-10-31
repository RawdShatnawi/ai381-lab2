# AI381 Lab 2 — Containerised Churn API

[![ci](https://github.com/RawdShatnawi/ai381-lab2/actions/workflows/ci.yml/badge.svg)](https://github.com/RawdShatnawi/ai381-lab2/actions/workflows/ci.yml)

A FastAPI service that serves the churn model from Lab 1. Multi-stage Dockerfile,
non-root container, HEALTHCHECK, and CI via GitHub Actions that scans with Trivy
and pushes to GHCR tagged with the commit SHA.

## One-command start

```bash
docker run -p 8000:8000 ghcr.io/rawdshathnawi/ai381-lab2:507a6c3eb84e7ab50d3b82e9220fbcbd3465332f
