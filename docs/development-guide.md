# Sofzenix eSign - Git & Engineering Guidelines (`docs/development-guide.md`)

---

## 1. Git Branching Strategy

The repository follows a clean branch-per-developer / feature-branch workflow:

```
main (stable integrated branch)
│
├── Anshul
├── developer-1
└── developer-2
```

### Branching Rules
1. `main` is the protected, stable integration branch. No direct pushes allowed to `main`.
2. Every developer creates their isolated branch (e.g. `Anshul`, `developer-1`, or `feature/identity-module`).
3. Merge requests into `main` require CI check passage and code review approval.

---

## 2. Commit Message Conventions

All commit messages MUST adhere to conventional commit standards. Use clear, meaningful commit titles describing the architectural intent.

### Standard Prefix Types
- `feat:` New capability or domain module addition.
- `fix:` Bug fix or path resolution.
- `docs:` Documentation or architecture specification update.
- `test:` Unit, integration, or contract test addition.
- `refactor:` Code restructuring without behavioral change.
- `chore:` Dependency update, build script modification.

### Recommended Commit Examples
```bash
feat: add document domain model
feat: add document upload API
feat: add workflow definition
test: add document service tests
docs: update workflow architecture
fix: correct document validation
```

### Commit Cleanliness Rules
- Do NOT create noisy, fragmented commits (e.g., "wip", "fixed typo", "test"). Squashing prior to merging is encouraged.
- Keep commits focused on a single logical change.

---

## 3. Secrets Management & Environment Security

> [!CAUTION]
> **NEVER COMMIT REAL SECRETS, API KEYS, OR CERTIFICATES TO GIT.**

1. Always use `.env` files for local runtime configuration.
2. Commit `.env.example` containing only placeholder variable names.
3. Pre-commit hooks will automatically scan for credential leaks before allowing git commits.
