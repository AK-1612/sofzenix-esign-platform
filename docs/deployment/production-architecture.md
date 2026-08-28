# Production Infrastructure & Kubernetes Specification

---

## 1. Kubernetes Production Architecture

Production environments deploy to managed K8s (EKS / GKE / AKS) with multi-AZ node redundancy.

- **Frontend Deployment**: 3 Replicas (Next.js Node Pods).
- **Backend Service Deployment**: Auto-scaled 3 to 10 Replicas (Spring Boot Java Pods).
- **AI Workspace Deployment**: Auto-scaled 2 to 6 Replicas with GPU node affinity for heavy OCR workloads.
- **Managed Databases**: AWS RDS PostgreSQL Multi-AZ & MongoDB Atlas Cluster.
- **Managed Cache**: AWS ElastiCache Redis Cluster.

---

## 2. SSL & Ingress Routing

Nginx Ingress Controller with Cert-Manager for automated Let's Encrypt TLS certificate generation and renewal.
