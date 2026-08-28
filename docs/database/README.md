# Database Architecture Documentation (`docs/database`)

---

## Overview

This directory documents the database modeling principles, multi-tenant database isolation strategies, indexing guidelines, and ORM mapping policies.

> [!IMPORTANT]
> **DATA MODELING FOLLOWS DOMAIN DESIGN**: Database table schemas, Flyway migrations, and ORM entity definitions are **intentionally not created** until domain requirements and API contracts are finalized in Phase 1.

---

## Directory Contents
- `data-modeling-guidelines.md`: Guidelines for modeling relational PostgreSQL schemas, MongoDB collections, and multi-tenant isolation.
