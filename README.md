# Demo AI Chatbot

Here’s a high-level walkthrough of how everything fits together, and the key technologies powering your server:

---

## 1. Server Architecture & Flow

1. **FastAPI Web Framework**

   * Handles HTTP routing and request/response lifecycle.
   * Lightweight, async-first design makes it easy to build performant APIs in Python.

2. **Uvicorn ASGI Server**

   * Runs your FastAPI app in production or development (`uvicorn.run("server:app",…)`).
   * Provides the asynchronous event loop and HTTP protocol handling.

3. **Rule-Based “Expert System” Logic**

   * On startup, the server loads a local JSON file (`knowledge_base.json`) into memory.
   * Each entry has a `"question"` keyword and an `"answer"`.
   * When a request comes in, the raw request body is decoded and interpreted as one of:

     * JSON (`{ "message": "..." }`)
     * URL-encoded form (`message=...`)
     * Plain text
   * The server then does a simple substring scan through the loaded questions.
   * If a keyword match is found, it immediately returns the associated answer.
   * Otherwise it replies with a default “I’m sorry…” fallback.

4. **CORS Middleware**

   * Configured via FastAPI’s `CORSMiddleware` so your browser-based frontend can talk to `http://localhost:8000` (or any origin) without preflight failures.

---

## 2. Key Server-Side Technologies

| Technology                  | Purpose                                                   |
| --------------------------- | --------------------------------------------------------- |
| **Python 3.10+**            | Language runtime                                          |
| **FastAPI**                 | Async web framework for defining endpoints and models     |
| **Uvicorn**                 | ASGI server to run FastAPI apps                           |
| **python-dotenv**           | Loads environment variables (e.g. API keys, configs)      |
| **json**                    | Built-in module to parse your `knowledge_base.json` file  |
| **urllib.parse**            | Parses URL-encoded form data when it arrives as text      |
| **fastapi.middleware.cors** | Allows AJAX calls from your HTML/JS widget without errors |

---

## 3. Frontend Workflow

1. **HTML/CSS/JavaScript** — No frameworks required.
2. A circular button toggles a chat “drawer” (styled with plain CSS).
3. The user types a message and clicks “▶” (or presses Enter).
4. JS builds a `URLSearchParams` payload or raw JSON, then does

   ```js
   fetch('/chat', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ message: text })
   })
   ```
5. The server’s universal body parser grabs the text, finds a rule, and returns `{ reply: "..." }`.
6. The JS appends the bot’s reply into the chat window.

---

### Why This Stack?

* **Simplicity**: Pure Python + JSON rules – no external AI calls.
* **Performance**: FastAPI + Uvicorn are built for asynchronous workloads.
* **Portability**: All logic lives in a single `server.py` and `knowledge_base.json`.
* **Zero-Dependency Frontend**: Vanilla HTML/JS means you can drop this widget into any site.

Let me know if you want to dive deeper into any part—pattern-matching logic, CORS policies, or customizing the UI!
