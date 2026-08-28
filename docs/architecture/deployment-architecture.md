# Deployment Architecture Specification

---

## 1. Containerization & Topology

The platform deployment topology leverages Docker containers managed by Kubernetes (K8s) for production environments and Docker Compose for local developer environments.

```
                                  ┌───────────────────────┐
                                  │      Cloudflare       │
                                  │   (Edge WAF & CDN)    │
                                  └───────────┬───────────┘
                                              │ HTTPS (Port 443)
                                              ▼
                                  ┌───────────────────────┐
                                  │     Nginx Ingress     │
                                  │      Controller       │
                                  └───────────┬───────────┘
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    │                                                   │
                    ▼                                                   ▼
┌───────────────────────────────────────┐   ┌───────────────────────────────────────┐
│     Frontend K8s Deployment           │   │     Backend API K8s Deployment        │
│    (Next.js Node Pods - 3 Replicas)   │   │    (Spring Boot Java Pods - Auto)     │
└───────────────────────────────────────┘   └───────────────────┬───────────────────┘
                                                                │
                                    ┌───────────────────────────┼───────────────────────────┐
                                    ▼                           ▼                           ▼
                        ┌───────────────────────┐   ┌───────────────────────┐   ┌───────────────────────┐
                        │ AI Service Pods       │   │ Managed PostgreSQL    │   │ Managed Redis & Kafka │
                        │ (FastAPI - GPU/CPU)   │   │ (AWS RDS / Azure DB)  │   │ (Cluster Instances)   │
                        └───────────────────────┘   └───────────────────────┘   └───────────────────────┘
```

---

## 2. Infrastructure Requirements

- **Kubernetes Ingress**: Manages SSL termination, path-based routing (`/api/v1/*` ➔ Backend, `/ai/*` ➔ AI Service, `/*` ➔ Frontend).
- **Auto-scaling (HPA)**: Horizontal Pod Autoscaler based on CPU (>70%) and Memory metrics.
- **Storage Mounting**: Ephemeral local scratch space for PDF rendering; permanent durable storage delegated exclusively to Object Storage (S3 / Azure Blob).
