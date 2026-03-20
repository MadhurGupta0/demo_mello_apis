import os

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request
from supabase import Client, create_client
from werkzeug.security import check_password_hash, generate_password_hash


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()
TABLE_NAME = "demo_mello_table"
EMAIL_COLUMN = "email"
PASSWORD_COLUMN = "password"
LOGIN_STATUS_COLUMN = "login"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



app = Flask(__name__)

API_DOCS_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>demo_mello_api — API Documentation</title>
    <style>
      :root {
        color-scheme: light dark;
        --bg: #0b1220;
        --panel: #111a2e;
        --text: #e6edf7;
        --muted: #aab6cc;
        --border: #25314d;
        --code: #0a0f1d;
        --accent: #7aa2ff;
        --good: #32d296;
        --warn: #ffcc66;
        --bad: #ff6b6b;
      }
      @media (prefers-color-scheme: light) {
        :root {
          --bg: #f6f8fc;
          --panel: #ffffff;
          --text: #0b1220;
          --muted: #42526e;
          --border: #d7deee;
          --code: #0b1220;
          --accent: #2b59ff;
        }
      }
      body {
        margin: 0;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto,
          Arial, "Apple Color Emoji", "Segoe UI Emoji";
        background: var(--bg);
        color: var(--text);
        line-height: 1.5;
      }
      .wrap {
        max-width: 980px;
        margin: 0 auto;
        padding: 28px 18px 64px;
      }
      header {
        padding: 18px 18px;
        border: 1px solid var(--border);
        background: var(--panel);
        border-radius: 14px;
      }
      h1 {
        margin: 0 0 6px;
        font-size: 22px;
        letter-spacing: 0.2px;
      }
      p {
        margin: 10px 0;
        color: var(--muted);
      }
      .grid {
        display: grid;
        gap: 14px;
        margin-top: 14px;
      }
      .card {
        border: 1px solid var(--border);
        background: var(--panel);
        border-radius: 14px;
        padding: 16px 16px 14px;
      }
      .topline {
        display: flex;
        align-items: baseline;
        gap: 10px;
        flex-wrap: wrap;
      }
      .method {
        font-weight: 700;
        padding: 2px 10px;
        border-radius: 999px;
        border: 1px solid var(--border);
        background: rgba(122, 162, 255, 0.12);
        color: var(--accent);
        font-size: 12px;
      }
      .path {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
          "Liberation Mono", "Courier New", monospace;
        font-size: 15px;
      }
      .desc {
        margin-top: 8px;
        color: var(--muted);
      }
      .cols {
        display: grid;
        grid-template-columns: 1fr;
        gap: 12px;
        margin-top: 12px;
      }
      @media (min-width: 860px) {
        .cols {
          grid-template-columns: 1fr 1fr;
        }
      }
      pre {
        margin: 0;
        padding: 12px 12px;
        overflow: auto;
        border-radius: 12px;
        border: 1px solid var(--border);
        background: var(--code);
        color: #e6edf7;
      }
      code {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
          "Liberation Mono", "Courier New", monospace;
        font-size: 12.5px;
      }
      .meta {
        display: grid;
        gap: 8px;
      }
      .pillrow {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
      }
      .pill {
        padding: 2px 10px;
        border-radius: 999px;
        border: 1px solid var(--border);
        background: rgba(255, 255, 255, 0.04);
        font-size: 12px;
        color: var(--muted);
      }
      .pill.ok {
        color: var(--good);
      }
      .pill.err {
        color: var(--bad);
      }
      .pill.warn {
        color: var(--warn);
      }
      a {
        color: var(--accent);
        text-decoration: none;
      }
      a:hover {
        text-decoration: underline;
      }
      .footer {
        margin-top: 18px;
        color: var(--muted);
        font-size: 12px;
      }
      .small {
        font-size: 12px;
      }
      .kbd {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
          "Liberation Mono", "Courier New", monospace;
        border: 1px solid var(--border);
        padding: 1px 6px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.04);
        color: var(--muted);
      }
      ul {
        margin: 8px 0 0;
        padding-left: 18px;
        color: var(--muted);
      }
    </style>
  </head>
  <body>
    <div class="wrap">
      <header>
        <h1>demo_mello_api — API Documentation</h1>
        <p>
          Base URL: <span class="kbd">https://new-mello-backend.thankfuldesert-772ce932.westus.azurecontainerapps.io</span> (default).
          All requests/responses are JSON unless stated otherwise.
        </p>
        <p class="small">
          Supabase table: <span class="kbd">demo_mello_table</span> • Typical
          columns used by the API: <span class="kbd">email</span>,
          <span class="kbd">password</span>, <span class="kbd">login</span>
        </p>
      </header>

      <div class="grid">
        <div class="card" id="health">
          <div class="topline">
            <span class="method">GET</span>
            <span class="path">/health</span>
          </div>
          <div class="desc">Simple server health check.</div>
          <div class="cols">
            <div class="meta">
              <div class="pillrow">
                <span class="pill ok">200 OK</span>
              </div>
              <p class="small">No request body.</p>
            </div>
            <pre><code>{
  "ok": true
}</code></pre>
          </div>
        </div>

        <div class="card" id="check-email">
          <div class="topline">
            <span class="method">POST</span>
            <span class="path">/check-email</span>
          </div>
          <div class="desc">
            Checks whether an email exists in <span class="kbd">demo_mello_table</span>.
          </div>
          <div class="cols">
            <div>
              <div class="pillrow">
                <span class="pill ok">200 OK</span>
                <span class="pill err">400 Invalid email</span>
                <span class="pill err">500 Supabase query failed</span>
              </div>
              <p class="small">Request JSON:</p>
              <pre><code>{
  "email": "test@example.com"
}</code></pre>
              <p class="small">Example curl (Windows):</p>
              <pre><code>curl -X POST https://new-mello-backend.thankfuldesert-772ce932.westus.azurecontainerapps.io/check-email ^
  -H "Content-Type: application/json" ^
  -d "{\\\"email\\\":\\\"test@example.com\\\"}"</code></pre>
            </div>
            <div>
              <p class="small">Response JSON:</p>
              <pre><code>{
  "email": "test@example.com",
  "exists": true
}</code></pre>
            </div>
          </div>
        </div>

        <div class="card" id="signup">
          <div class="topline">
            <span class="method">POST</span>
            <span class="path">/signup</span>
          </div>
          <div class="desc">
            Creates a new user row and sets <span class="kbd">login_status</span> to
            <span class="kbd">true</span>. Passwords are stored as a hash.
          </div>
          <div class="cols">
            <div>
              <div class="pillrow">
                <span class="pill ok">201 Created</span>
                <span class="pill err">400 Validation errors</span>
                <span class="pill warn">409 Email already exists</span>
                <span class="pill err">500 Signup failed</span>
              </div>
              <p class="small">Request JSON:</p>
              <pre><code>{
  "email": "test@example.com",
  "password": "secret",
  "confirm_password": "secret"
}</code></pre>
              <p class="small">Example curl (Windows):</p>
              <pre><code>curl -X POST https://new-mello-backend.thankfuldesert-772ce932.westus.azurecontainerapps.io/signup ^
  -H "Content-Type: application/json" ^
  -d "{\\\"email\\\":\\\"test@example.com\\\",\\\"password\\\":\\\"secret\\\",\\\"confirm_password\\\":\\\"secret\\\"}"</code></pre>
            </div>
            <div>
              <p class="small">Success response JSON:</p>
              <pre><code>{
  "created": true,
  "email": "test@example.com",
  "login_status": true
}</code></pre>
              <p class="small">Notes:</p>
              <ul>
                <li>
                  The API inserts <span class="kbd">password_hash</span> and does not
                  return it.
                </li>
                <li>
                  Supabase RLS policies must allow inserts/updates for your key.
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="card" id="login">
          <div class="topline">
            <span class="method">POST</span>
            <span class="path">/login</span>
          </div>
          <div class="desc">
            Verifies the password for the email and sets
            <span class="kbd">login_status</span> to <span class="kbd">true</span>.
          </div>
          <div class="cols">
            <div>
              <div class="pillrow">
                <span class="pill ok">200 OK</span>
                <span class="pill err">400 Validation errors</span>
                <span class="pill err">401 Invalid email or password</span>
                <span class="pill err">500 Login failed</span>
              </div>
              <p class="small">Request JSON:</p>
              <pre><code>{
  "email": "test@example.com",
  "password": "secret"
}</code></pre>
              <p class="small">Example curl (Windows):</p>
              <pre><code>curl -X POST https://new-mello-backend.thankfuldesert-772ce932.westus.azurecontainerapps.io/login ^
  -H "Content-Type: application/json" ^
  -d "{\\\"email\\\":\\\"test@example.com\\\",\\\"password\\\":\\\"secret\\\"}"</code></pre>
            </div>
            <div>
              <p class="small">Success response JSON:</p>
              <pre><code>{
  "email": "test@example.com",
  "login_status": true
}</code></pre>
            </div>
          </div>
        </div>

        <div class="card" id="logout">
          <div class="topline">
            <span class="method">POST</span>
            <span class="path">/logout</span>
          </div>
          <div class="desc">
            Sets <span class="kbd">login_status</span> to <span class="kbd">false</span>
            for the provided email.
          </div>
          <div class="cols">
            <div>
              <div class="pillrow">
                <span class="pill ok">200 OK</span>
                <span class="pill err">400 Invalid email</span>
                <span class="pill err">500 Logout failed</span>
              </div>
              <p class="small">Request JSON:</p>
              <pre><code>{
  "email": "test@example.com"
}</code></pre>
              <p class="small">Example curl (Windows):</p>
              <pre><code>curl -X POST https://new-mello-backend.thankfuldesert-772ce932.westus.azurecontainerapps.io/logout ^
  -H "Content-Type: application/json" ^
  -d "{\\\"email\\\":\\\"test@example.com\\\"}"</code></pre>
            </div>
            <div>
              <p class="small">Success response JSON:</p>
              <pre><code>{
  "email": "test@example.com",
  "login_status": false
}</code></pre>
            </div>
          </div>
        </div>
      </div>

      <div class="footer">
        Generated for the endpoints defined in <span class="kbd">app.py</span>.
        Open this file locally in a browser, or serve it as a static file if desired.
      </div>
    </div>
  </body>
</html>
"""


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.get("/docs")
def docs():
    return Response(API_DOCS_HTML, mimetype="text/html")


@app.post("/check-email")
def check_email():
    payload = request.get_json(silent=True) or {}
    email = str(payload.get("email", "")).strip().lower()
    if not email or "@" not in email:
        return jsonify({"error": "Invalid email"}), 400

    try:
        # Only fetch one row (minimal data) to check existence.
        resp = (
            supabase.table(TABLE_NAME)
            .select(EMAIL_COLUMN)
            .eq(EMAIL_COLUMN, email)
            .limit(1)
            .execute()
        )
        data = resp.data or []
        return jsonify({"email": email, "exists": len(data) > 0})
    except Exception as e:
        # Common causes: wrong key/url, RLS blocking reads, wrong table/column name.
        return jsonify({"error": "Supabase query failed", "details": str(e)}), 500


@app.post("/signup")
def signup():
    payload = request.get_json(silent=True) or {}
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))
    confirm_password = str(payload.get("confirm_password", ""))

    if not email or "@" not in email:
        return jsonify({"error": "Invalid email"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    try:
        
        password_hash = generate_password_hash(password)
        insert_resp = (
            supabase.table(TABLE_NAME)
            .insert(
                {
                    EMAIL_COLUMN: email,
                    PASSWORD_COLUMN: password_hash,
                    LOGIN_STATUS_COLUMN: True,
                }
            )
            .execute()
        )

        row = (insert_resp.data or [{}])[0]
        return (
            jsonify(
                {
                    "created": True,
                    "email": row.get(EMAIL_COLUMN, email),
                    "login_status": row.get(LOGIN_STATUS_COLUMN, True),
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": "Signup failed", "details": str(e)}), 500


@app.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))

    if not email or "@" not in email:
        return jsonify({"error": "Invalid email"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    try:
        resp = (
            supabase.table(TABLE_NAME)
            .select(f"{EMAIL_COLUMN},{PASSWORD_COLUMN},{LOGIN_STATUS_COLUMN}")
            .eq(EMAIL_COLUMN, email)
            .limit(1)
            .execute()
        )
        rows = resp.data or []
        if not rows:
            return jsonify({"error": "Invalid email or password"}), 401

        row = rows[0]
        stored_hash = row.get(PASSWORD_COLUMN) or ""
        if not stored_hash or not check_password_hash(stored_hash, password):
            return jsonify({"error": "Invalid email or password"}), 401

        supabase.table(TABLE_NAME).update({LOGIN_STATUS_COLUMN: True}).eq(
            EMAIL_COLUMN, email
        ).execute()

        return jsonify({"email": email, "login_status": True})
    except Exception as e:
        return jsonify({"error": "Login failed", "details": str(e)}), 500


@app.post("/logout")
def logout():
    payload = request.get_json(silent=True) or {}
    email = str(payload.get("email", "")).strip().lower()

    if not email or "@" not in email:
        return jsonify({"error": "Invalid email"}), 400

    try:
        supabase.table(TABLE_NAME).update({LOGIN_STATUS_COLUMN: False}).eq(
            EMAIL_COLUMN, email
        ).execute()
        return jsonify({"email": email, "login_status": False})
    except Exception as e:
        return jsonify({"error": "Logout failed", "details": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)
