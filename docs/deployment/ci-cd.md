# Continuous Integration & Delivery (CI/CD) Architecture

---

## 1. Pipeline Stages

The GitHub Actions CI/CD pipeline (`.github/workflows/ci.yml`) executes automated checks on pull requests:

```
[Push / PR] ──► Linting & Static Analysis ──► Unit & Component Tests ──► Security Scan ──► Container Build
```

---

## 2. Environment Promotion Strategy

- **`main` Branch**: Triggers automated deployment to the Staging Environment.
- **Release Tags (`v*.*.*`)**: Triggers Production deployment after manual release approval gate.
