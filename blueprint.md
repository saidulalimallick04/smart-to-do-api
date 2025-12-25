# Project Blueprint: Smart To Do API - 10-Phase Development Journey

This document outlines the 10 distinct phases of development for the Smart To Do API, ensuring a robust, user-centric, and high-quality solution.

## Phase 1: Conceptualization & "Smart" Definition

**Goal:** Define the core identity and unique value proposition.

- **Philosophy**: A backend that "understands" the user, offering "helpful" error messages instead of raw stack traces.
- **Smart Logic**: Auto-inference of task metadata (tags, priority) using key-phrase matching (implemented in `core/utils.py`).

## Phase 2: Architecture & System Design

**Goal:** Establish the technical foundation.

- **ODM**: **Beanie** (built on top of Motor) for asynchronous, type-safe MongoDB interactions.
- **Structure**: modular "Service-Repository" pattern style:
  - `api/v1/endpoints`: Route handlers.
  - `schemas`: Pydantic V2 definitions for validation.
  - `models`: Database document definitions.

## Phase 3: Environment & Security Setup

**Goal:** Prepare the secure development environment.

- **Dependency Management**: Uses `uv` for blazing fast package resolution.
- **Configuration**: `colre/config.py` loads settings from `.env` using `pydantic-settings`.
- **Secrets**: `REFRESH_TOKEN_EXPIRE_DAYS` and `ACCESS_TOKEN_EXPIRE_MINUTES` are fully configurable.

## Phase 4: Database Core & Models

**Goal:** Connect to the data layer.

- **Async Session**: `db/mongodb.py` handles the `MotorClient` lifecycle.
- **Models**:
  - `User`: Handles auth info (`hashed_password`) and profile data.
  - `Task`: Includes `priority` (High/Medium/Low) and `tags` (List[str]).

## Phase 5: Authentication Engine

**Goal:** Secure the system with modern standard.

- **JWT Strategy**: Dual-token system (Access + Refresh).
- **Smart Rotation**: Refresh tokens are only rotated if they are within 2 days of expiration (configurable), reducing write operations while maintaining security.
- **Request Body**: Refresh tokens are securely passed in the JSON body, not query parameters.

## Phase 6: Task Management System (CRUD)

**Goal:** Implement core business logic.

- **Endpoints**:
  - `POST /tasks`: Uses `infer_task_metadata` to auto-populate fields.
  - `GET /tasks`: Supports pagination (`skip`, `limit`) and filtering (`is_completed`, `priority`).
  - `GET/PUT/DELETE /tasks/{id}`: Full resource lifecycle management.

## Phase 7: "Smart" Features Integration

**Goal:** Differentiate the product.

- **Inference Engine**: `core/utils.py` scans task descriptions for keywords (e.g., "urgent" -> High Priority, "buy" -> "shopping" tag).
- **Helpful Responses**: Global exception handlers in `main.py` catch 401/404 errors and return conversational messages.

## Phase 8: Refinement & Advanced Logic

**Goal:** Polish the API interaction.

- **Pagination**: Implemented on listing endpoints.
- **Sorting/Filtering**: Query parameters allow precise data retrieval.
- **Error Handling**: Custom exception handlers ensure no raw internal errors leak to the client.

## Phase 9: Quality Assurance & Testing

**Goal:** Verify robustness.

- **Test Runner**: `pytest` paired with `AnyIO` for async testing.
- **Coverage**:
  - `test_auth.py`: Covers Signup, Login, and specific Refresh Token logic.
  - `test_tasks.py`: Full CRUD lifecycle verification.

## Phase 10: Documentation & Final Delivery

**Goal:** Prepare for hand-off.

- **README.md**: Comprehensive setup guide, architecture diagram, and tech stack.
- **API Documentation**: Detailed endpoint breakdown in `API_DOCUMENTATION.md`.
- **Postman**: Ready-to-use `postman_collection.json` with environment variables.
