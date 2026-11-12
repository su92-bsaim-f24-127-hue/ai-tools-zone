# Phase 4.3 — Proprietary `.cursorrules` Blueprints & Prompt Engineering Pack
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Classification:** Proprietary Work of Authorship (Owned by AI Tools Zone)  
**Permitted Commercial Mode:** Client Consulting Deliverable (Tier 2 Advanced Setup)  
**Production Authorization:** STRICTLY NOT GRANTED

---

## 1. Intellectual Property & License Notice
The configuration templates and prompt engineering blueprints contained herein are original works of authorship created by AI Tools Zone technical staff. They are licensed exclusively to paying consulting clients for internal development use. Redistribution or commercial resale by third parties is prohibited.

---

## 2. Production `.cursorrules` Blueprints

### Blueprint 1: Next.js 15 & React Full-Stack Architecture
*Target Stack: Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS, Server Actions, Prisma/Supabase.*

```markdown
# AI Tools Zone - Next.js 15 Full-Stack Configuration Rules
# (c) 2026 AI Tools Zone. Client Consulting License.

You are an expert full-stack Next.js 15, React 19, TypeScript, and Tailwind CSS engineer.

## Architecture & Code Structure
- Always use the Next.js App Router (`app/` directory).
- Default to React Server Components (RSC). Only mark components with `'use client'` when using state, hooks, or browser event listeners.
- Keep server actions in dedicated files (e.g., `app/actions/`) marked with `'use server'`.
- Validate all incoming server action data using Zod schemas before database execution.
- Use TypeScript strict mode with explicit interfaces. Never use `any`.

## Styling & UI Guidelines
- Use Tailwind CSS utility classes exclusively. Avoid raw CSS files or inline style objects.
- Ensure all interactive elements have responsive layouts, accessible ARIA attributes, and hover/focus-visible states.
- Follow mobile-first responsive breakpoints (`sm:`, `md:`, `lg:`, `xl:`).

## Performance & Security
- Optimize image delivery using `next/image` with explicit `width`, `height`, and priority attributes for LCP images.
- Protect all API routes and Server Actions with authenticated session checks.
- Never hardcode API keys, secrets, or database URLs in source code. Reference environment variables via `process.env.NEXT_PUBLIC_*` or server-only `process.env.*`.
```

---

### Blueprint 2: Python, FastAPI & Asynchronous Backend Architecture
*Target Stack: Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy (Async), Alembic, Pytest.*

```markdown
# AI Tools Zone - FastAPI & Python Architecture Rules
# (c) 2026 AI Tools Zone. Client Consulting License.

You are an expert Python 3.12+ backend architect specializing in FastAPI, Pydantic v2, and async SQLAlchemy.

## Code Standards & Conventions
- Write clean, modular, object-oriented, and type-annotated Python code adhering strictly to PEP 8.
- Use Pydantic v2 `BaseModel` schemas for all request validation and response models.
- Always implement explicit type hints (`typing.Optional`, `typing.List`, `typing.Annotated`).
- Utilize asynchronous handlers (`async def`) for I/O-bound database queries and HTTP requests.

## Database & ORM Rules
- Use AsyncSession with SQLAlchemy 2.0+ syntax (`select()`, `scalars()`).
- Never perform blocking synchronous operations inside an async route handler.
- Handle database transactions within context managers with automatic rollback on exception.

## Testing & Error Handling
- Use standard FastAPI `HTTPException` with explicit status codes and error detail payloads.
- Write unit and integration tests using `pytest` and `httpx.AsyncClient`.
- Maintain docstrings following Google Python Style Guide for all service functions.
```

---

## 3. Curated Prompt Engineering Pack (Client Reference)

### Prompt Pack 1: Test-Driven Generation Pattern (TDD)
> *"Given the following TypeScript interface and business requirements:  
> [PASTE INTERFACE / REQUIREMENTS]  
> Generate a comprehensive Pytest / Vitest test suite that covers:  
> 1. Happy path execution with valid inputs.  
> 2. Boundary edge cases (empty arrays, maximum string lengths, null inputs).  
> 3. Negative error cases with expected exceptions and error messages.  
> Write clean, readable assertions with descriptive test titles. Do not write the implementation code yet."*

### Prompt Pack 2: Performance & Token Optimization Pattern
> *"Analyze the following function for algorithmic bottlenecks, redundant database queries, and memory leaks:  
> [PASTE CODE]  
> Refactor the code to:  
> 1. Reduce time complexity from O(n^2) to O(n) or O(n log n).  
> 2. Implement batching or caching where applicable.  
> 3. Provide a brief explanation of before-vs-after computational complexity."*

### Prompt Pack 3: Secure API Route Boilerplate Generator
> *"Generate a production-ready Next.js / FastAPI route handler for the following endpoint:  
> [SPECIFY ROUTE, E.G., POST /api/v1/orders]  
> Requirements:  
> 1. Strict input validation using Zod / Pydantic.  
> 2. Authentication check and rate-limiting middleware.  
> 3. Structured error responses matching standard RFC 7807 problem details.  
> 4. Structured logging for audit compliance."*
