# Containerization Standards and Best Practices

This document outlines Bayat's standards for containerization, primarily focusing on Docker and related technologies.

## Table of Contents

- [Overview](#overview)
- [Docker Standards](#docker-standards)
  - [Base Images](#base-images)
  - [Dockerfile Standards](#dockerfile-standards)
  - [Image Tagging Conventions](#image-tagging-conventions)
  - [Multi-stage Builds](#multi-stage-builds)
  - [Image Security](#image-security)
- [Container Orchestration](#container-orchestration)
  - [Kubernetes Standards](#kubernetes-standards)
  - [Docker Compose Standards](#docker-compose-standards)
- [Container Registry](#container-registry)
- [Development Workflow](#development-workflow)
- [Production Considerations](#production-considerations)
- [Security Best Practices](#security-best-practices)
- [Performance Optimization](#performance-optimization)
- [Monitoring and Logging](#monitoring-and-logging)
- [Common Anti-patterns](#common-anti-patterns)

## Overview

Containerization is a core part of Bayat's deployment strategy. This document provides guidelines for creating, managing, and deploying containers in a consistent and secure manner across all projects.

## Docker Standards

### Base Images

- **Use official base images** whenever possible
- **Prefer Alpine-based images** for smaller footprints when appropriate
- **Standardized base images** for each language/framework:
  - Node.js: `node:18-alpine` (or current LTS Alpine version)
  - Python: `python:3.10-slim` (or current stable slim version)
  - .NET: `mcr.microsoft.com/dotnet/sdk:6.0` for build, `mcr.microsoft.com/dotnet/aspnet:6.0` for runtime
  - Java: `eclipse-temurin:17-jre-alpine` (or current LTS Alpine version)
- **Pin exact versions** for reproducible builds (e.g., `node:18.12.1-alpine`)
- **Regularly update base images** to incorporate security patches

### Dockerfile Standards

- **One responsibility per container** - follow single-concern principle
- **Order instructions** from least to most frequently changing to maximize caching
- **Use .dockerignore** to exclude unnecessary files
- **Minimize layer count** by combining related RUN commands with `&&`
- **Set appropriate USER** - avoid running as root when possible
- **Include metadata** using LABEL directives:
  ```dockerfile
  LABEL org.bayat.project="<project-name>"
  LABEL org.bayat.version="<version>"
  LABEL org.bayat.maintainer="<team-email>"
  ```
- **Define HEALTHCHECK** instructions for production containers
- **Set WORKDIR** instead of using `RUN cd /path`

### Image Tagging Conventions

- **Use semantic versioning** for release tags (`1.0.0`, `1.0.1`, etc.)
- **Use git SHA for development builds** (`git-abc1234`)
- **Use `latest` tag sparingly** and only for development environments
- **Include environment/purpose in tags** when appropriate (`1.0.0-staging`, `1.0.0-production`)

### Multi-stage Builds

- **Use multi-stage builds** to separate build and runtime environments
- **Name stages** using the `AS <stage-name>` syntax for clarity
- **Copy only necessary artifacts** between stages
- **Example multi-stage pattern**:
  ```dockerfile
  # Build stage
  FROM node:18-alpine AS build
  WORKDIR /app
  COPY package*.json ./
  RUN npm ci
  COPY . .
  RUN npm run build
  
  # Runtime stage
  FROM node:18-alpine AS runtime
  WORKDIR /app
  COPY --from=build /app/dist ./dist
  COPY --from=build /app/package*.json ./
  RUN npm ci --only=production
  USER node
  CMD ["node", "dist/index.js"]
  ```

### Image Security

- **Scan all images** for vulnerabilities before pushing to registry
- **Remove development dependencies** from production images
- **Don't store secrets in images** - use environment variables or secret management solutions
- **Keep images updated** with the latest security patches

## Container Orchestration

### Kubernetes Standards

- **Use Helm charts** for packaging Kubernetes applications
- **Follow resource definition structure**:
  - Deployments/StatefulSets
  - Services
  - ConfigMaps
  - Secrets
  - Ingress resources
- **Set resource limits and requests** for all containers
- **Use namespaces** to organize applications
- **Implement proper liveness and readiness probes**
- **Use network policies** to restrict communication

### Docker Compose Standards

- **Use docker-compose for development environments**
- **Version**: Use docker-compose file format version 3 or later
- **Service naming**: Use clear, descriptive service names
- **Volume mounts**: Follow the pattern `./local/path:/container/path`
- **Environment variables**: Use `.env` files for environment-specific configurations
- **Networks**: Define custom networks for service isolation

## Container Registry

- **Use centralized registry** for all container images
- **Implement access controls** on the registry
- **Automate vulnerability scanning** for all images
- **Set image retention policies** to manage storage
- **Tag images clearly** following the conventions described above

## Development Workflow

- **Use Docker Compose** for local development environments
- **Consistent development/production parity** to minimize "works on my machine" issues
- **Hot-reloading** for development containers where appropriate
- **Local volume mounts** for development:
  ```yaml
  volumes:
    - ./src:/app/src
  ```
- **Document environment variables** needed for each container

## Production Considerations

- **Immutable infrastructure** - don't modify running containers
- **Implement circuit breakers and retry mechanisms** for resilience
- **Use rolling updates** for zero-downtime deployments
- **Implement proper backup strategies** for stateful containers
- **Monitor container health and performance**
- **Set appropriate restart policies**

## Security Best Practices

- **Run containers with the minimum required privileges**
- **Use non-root users** inside containers
- **Implement read-only file systems** where possible
- **Use network segmentation** to limit container communication
- **Apply security context settings** in Kubernetes
- **Regularly update and patch container images**
- **Scan images for vulnerabilities** before deployment
- **Implement runtime security monitoring**

## Performance Optimization

- **Minimize image size** to improve pull times and reduce attack surface
- **Optimize caching** for faster builds
- **Use appropriate resource limits** to prevent resource contention
- **Benchmark and profile** container performance regularly
- **Optimize startup time** for faster scaling and deployments

## Monitoring and Logging

- **Implement centralized logging** for all containers
- **Use structured logging** (JSON format)
- **Configure log rotation** to manage disk usage
- **Expose metrics endpoints** for monitoring systems
- **Implement tracing** for distributed systems
- **Monitor container resource usage**

## Common Anti-patterns

Avoid these common containerization mistakes:

- Running as root unnecessarily
- Storing sensitive data in images
- Using the `latest` tag in production
- Not setting resource limits
- Creating overly large images
- Running multiple processes in a single container
- Hardcoding configuration in images
- Not implementing health checks
- Using host networking without a clear reason
- Mounting sensitive host directories

## References

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Container Security Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html) 