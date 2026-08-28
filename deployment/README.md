# Infrastructure Deployment Scaffold (`deployment/`)

---

## Directory Overview

This directory holds infrastructure-as-code manifests, Helm charts, Dockerfiles, and Nginx gateway configurations for deploying the Sofzenix platform across local, staging, and production Kubernetes clusters.

### Targeted Sub-structures
- `docker/`: Base Dockerfiles for Frontend, Backend, and AI Workspace containers.
- `helm/`: Helm charts for Spring Boot Backend, FastAPI AI Service, and Ingress routing.
- `k8s/`: Plain Kubernetes YAML manifests (Deployments, StatefulSets, Services, ConfigMaps, Secrets).
- `nginx/`: Nginx API Gateway ingress and reverse proxy configuration files.

> Status: Scaffolding baseline for future Phase 10 deployment hardening.
