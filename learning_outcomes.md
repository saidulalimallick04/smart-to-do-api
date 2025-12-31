# 🎓 Learning Outcomes: Smart To Do API

This document summarizes the key technical concepts, libraries, and architectural decisions explored during the development of the **Smart To Do API**. It serves as a knowledge base for understanding the "Why" and "How" behind the project.

---

## 🏗️ 1. Core Architecture & Design Patterns

### **Service-Repository Pattern (Simplified)**

Instead of putting all logic in routes, we separated concerns:

- **`models/`**: Defines the data structure (Database layer).
- **`schemas/`**: Defines what data is allowed in/out (Validation layer).
- **`api/v1/endpoints/`**: Handles user requests and connects the layers.
- **Why?**: This makes the code modular, testable, and easier to maintain.

### **Asynchronous I/O**

We built the entire application using Python's `async/await` syntax.

- **Impact**: Allows the server to handle thousands of concurrent connections (like DB queries) without blocking the main thread.
- **Key usage**: `async def create_task(...)` limits waiting time for MongoDB operations.

---

## 🛠️ 2. Key Libraries & Tools

| Library | Purpose | Why we chose it? |
| :--- | :--- | :--- |
| **FastAPI** | Web Framework | Fastest Python framework, auto-generates Swagger docs, and natively supports async. |
| **Beanie** | MongoDB ODM | Built on Pydantic & Motor. Offers type safety and developer productivity (no raw queries). |
| **Motor** | Async DB Driver | The bridge between Python's async loop and MongoDB. |
| **Pydantic V2** | Data Validation | Strict typing for API inputs. V2 is Rust-based and significantly faster than V1. |
| **PyJWT** | Authentication | Industry standard for stateless authentication (Access + Refresh tokens). |
| **Passlib** | Security | Handles password hashing (Bcrypt) to ensure no plain-text passwords are stored. |
| **Uvicorn** | ASGI Server | Lightning-fast ASGI server to run the FastAPI application. |
| **uv** | Package Manager | A modern, high-performance replacement for `pip`. |

---

## 🧠 3. Advanced Concepts Implemented

### **Smart Context Inference**

- **Concept**: The system "reads" the user's input to guess their intent.
- **Implementation**: We created a utility (`core/utils.py`) that scans for keywords in `title` and `description`.
- **Example**:
  - Input: *"Buy milk ASAP"*
  - Result: Tags -> `["shopping"]`, Priority -> `High`

### **Dual-Token Authentication (Smart Rotation)**

- **Concept**: Security vs. UX trade-off.
- **Implementation**:
  - **Access Token**: Short-lived (30 mins) for security.
  - **Refresh Token**: Long-lived (7 days) for convenience.
  - **Smart Rotation**: We don't rotate the refresh token on *every* request. We only issue a new one if it expires in < 2 days. This saves database writes while keeping rotation secure.

### **Glassmorphism & DevX**

- **Concept**: Developer Experience isn't just code; it's presentation.
- **Implementation**: Created a custom HTML/CSS Landing Page (`templates/index_jinja.html`) served at the root URL to give a professional first impression.

---

## 📂 4. Project Structure Explained

```bash
smart-to-do-api/
├── api/             # All route handlers (The "Controller")
├── core/            # Config, Security, and Utils (The "Backbone")
├── db/              # Database connection logic
├── models/          # Database Tables/Documents (The "Data")
├── schemas/         # Pydantic Schemas (The "Interface")
├── templates/       # HTML files for UI (Landing Page)
└── tests/           # Automated tests to ensure reliability
```

---

## 🚀 5. Deployment

- **Platform**: Vercel
- **Configuration**: Use `vercel.json` to tell Vercel how to handle Python requests (rewriting routes to `main.py`).
- **Outcome**: A serverless, globally distributed API accessible via HTTPS.
