# Sofzenix eSign - Frontend Web Application Scaffold

> Modern React / Next.js + TypeScript + Tailwind CSS Frontend Application Architecture.

---

## Overview

The `frontend/` directory contains the scaffold for the Sofzenix client application. It provides an intuitive, high-performance interface for document creation, signature workflows, workflow execution tracking, template design, AI contract insights, and administrative setup.

---

## Tech Stack
- **Framework**: Next.js / React (TypeScript)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **State & Data Fetching**: React Query / Context API (To be implemented in feature phase)

---

## Directory Architecture

```
frontend/
├── public/                 # Static public assets (favicons, brand logos)
├── src/
│   ├── assets/             # Images, custom fonts, global CSS styles
│   ├── components/         # Reusable atomic UI components (Buttons, Modals, Tables)
│   ├── hooks/              # Custom React hooks (auth, signature canvas, API state)
│   ├── layouts/            # Page layouts (DashboardLayout, AuthLayout, WorkflowLayout)
│   ├── pages/              # Application views & Next.js page routes
│   ├── routes/             # Client-side routing definitions & navigation guards
│   ├── services/           # HTTP API client abstractions (Axios/Fetch layer)
│   ├── types/              # TypeScript interface & type definitions
│   └── utils/              # Pure utility functions (formatters, validators, date helpers)
├── package.json            # Node.js dependencies configuration
└── README.md               # Frontend architectural documentation
```

---

## Status & Guidelines

> [!IMPORTANT]
> **NO BUSINESS LOGIC OR FAKE API CALLS**: This folder contains structural scaffolding only. No UI components or mock API responses are implemented yet.
