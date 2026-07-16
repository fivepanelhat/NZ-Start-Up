"""
Local Founder Console — localhost-only dashboard.

Not multi-tenant SaaS. Binds to 127.0.0.1 only.
G11: optional/required session token so local processes cannot browse company data freely.
Never sends email, files government forms, or moves money.
"""
from __future__ import annotations

import hmac
import html
import json
import os
import secrets
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, urlparse

from nz_startup import __version__, board_pack, calendar_ops, export_reminders, grants, memory, pipeline, status, weekly
from nz_startup.paths import companies_dir, company_dir

# Process-scoped session token (set at run_console); also accepts NZ_STARTUP_CONSOLE_TOKEN env
_CONSOLE_TOKEN: str = ""
_COOKIE_NAME = "nz_startup_console"


def _expected_token() -> str:
    return _CONSOLE_TOKEN or os.environ.get("NZ_STARTUP_CONSOLE_TOKEN", "").strip()


def _parse_cookies(header: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in (header or "").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def _esc(s: Any) -> str:
    return html.escape("" if s is None else str(s))


def _layout(title: str, body: str, flash: str = "") -> str:
    flash_html = f'<div class="flash">{_esc(flash)}</div>' if flash else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{_esc(title)} · NZ Start-Up Console</title>
  <style>
    :root {{
      --bg: #0b1220; --card: #111827; --text: #e5e7eb; --muted: #9ca3af;
      --accent: #38bdf8; --ok: #4ade80; --warn: #fbbf24; --bad: #f87171; --line: #1f2937;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; font-family: Inter, ui-sans-serif, system-ui, sans-serif;
      background: radial-gradient(1200px 600px at 10% -10%, #0ea5e933, transparent),
                  radial-gradient(900px 500px at 100% 0%, #a855f722, transparent), var(--bg);
      color: var(--text); min-height: 100vh;
    }}
    header {{
      padding: 1rem 1.5rem; border-bottom: 1px solid var(--line);
      display: flex; gap: 1rem; flex-wrap: wrap; align-items: center; justify-content: space-between;
    }}
    header a {{ color: var(--accent); text-decoration: none; margin-right: 1rem; }}
    main {{ max-width: 1000px; margin: 0 auto; padding: 1.5rem; }}
    .card {{
      background: color-mix(in srgb, var(--card) 92%, transparent);
      border: 1px solid var(--line); border-radius: 14px; padding: 1.25rem; margin-bottom: 1rem;
      backdrop-filter: blur(8px);
    }}
    h1,h2 {{ margin: 0 0 .75rem; }}
    .muted {{ color: var(--muted); }}
    .score {{ font-size: 2rem; font-weight: 700; color: var(--accent); }}
    table {{ width: 100%; border-collapse: collapse; font-size: .95rem; }}
    th, td {{ text-align: left; padding: .5rem .4rem; border-bottom: 1px solid var(--line); vertical-align: top; }}
    .ok {{ color: var(--ok); }} .gap {{ color: var(--bad); }}
    form.inline {{ display: inline; margin-right: .35rem; }}
    button, .btn {{
      background: #0369a1; color: white; border: 0; border-radius: 8px;
      padding: .45rem .8rem; cursor: pointer; font-weight: 600; font-size: .9rem;
    }}
    button.secondary {{ background: #334155; }}
    .flash {{
      background: #14532d55; border: 1px solid #22c55e66; padding: .75rem 1rem;
      border-radius: 10px; margin-bottom: 1rem;
    }}
    code, pre {{ background: #0f172a; padding: .1rem .35rem; border-radius: 4px; }}
    pre {{ padding: .75rem; overflow: auto; white-space: pre-wrap; font-size: .85rem; }}
    ul {{ padding-left: 1.2rem; }}
    .grid {{ display: grid; gap: 1rem; grid-template-columns: 1fr; }}
    @media (min-width: 800px) {{ .grid-2 {{ grid-template-columns: 1fr 1fr; }} }}
    footer {{ max-width: 1000px; margin: 2rem auto; padding: 0 1.5rem 2rem; color: var(--muted); font-size: .9rem; }}
  </style>
</head>
<body>
  <header>
    <div>
      <strong>NZ Start-Up Console</strong>
      <span class="muted"> v{_esc(__version__)} · localhost only</span>
    </div>
    <nav>
      <a href="/">Companies</a>
      <a href="/help">Help</a>
    </nav>
  </header>
  <main>
    {flash_html}
    {body}
  </main>
  <footer>
    Agents inform, draft, prepare, monitor, and remind.
    Humans advise, sign, file, send, and pay.
    This console never emails, files IRD/Companies Office, or moves money.
  </footer>
</body>
</html>"""


def _list_companies() -> list[str]:
    return memory.list_companies()


def _read_md(company_id: str, rel: str, limit: int = 2500) -> str:
    path = company_dir(company_id) / rel
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[:limit]


def page_home(flash: str = "") -> str:
    companies = _list_companies()
    rows = ""
    if not companies:
        rows = (
            "<tr><td colspan='3' class='muted'>No companies yet. "
            "Run <code>nz-startup onboard my-co</code></td></tr>"
        )
    else:
        for c in companies:
            try:
                st = status.collect_status(c)
                score = f"{st.get('score')}/100"
                band = st.get("band")
            except Exception:  # noqa: BLE001
                score, band = "—", "—"
            rows += (
                f"<tr><td><a href='/c/{_esc(c)}'>{_esc(c)}</a></td>"
                f"<td>{_esc(score)} <span class='muted'>({_esc(band)})</span></td>"
                f"<td><a class='btn' href='/c/{_esc(c)}'>Open</a></td></tr>"
            )
    body = f"""
    <div class="card">
      <h1>Founder companies</h1>
      <p class="muted">Local memory under <code>memory/companies/</code>. Not multi-tenant SaaS.</p>
      <table>
        <thead><tr><th>Company id</th><th>Status</th><th></th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <div class="card">
      <h2>CLI quick paths</h2>
      <ul>
        <li><code>nz-startup onboard my-startup --legal-name "…"</code></li>
        <li><code>nz-startup demo run --partner "Venture Taranaki"</code></li>
        <li><code>nz-startup board pack my-startup</code></li>
        <li><code>nz-startup pilot offer my-startup --customer "…"</code></li>
      </ul>
    </div>
    """
    return _layout("Home", body, flash)


def page_company(company_id: str, flash: str = "") -> str:
    try:
        st = status.collect_status(company_id)
    except FileNotFoundError:
        return _layout(
            "Missing",
            f"<div class='card'><h1>Unknown company</h1><p>{_esc(company_id)}</p>"
            f"<p><a href='/'>Back</a></p></div>",
        )

    checks = ""
    for c in st.get("checks") or []:
        cls = "ok" if c.get("ok") else "gap"
        mark = "OK" if c.get("ok") else "GAP"
        checks += (
            f"<tr><td class='{cls}'>{mark}</td><td>{_esc(c.get('area'))}</td>"
            f"<td class='muted'>{_esc(c.get('detail'))}</td></tr>"
        )
    actions = "".join(f"<li>{_esc(a)}</li>" for a in (st.get("next_actions") or [])[:8])
    if not actions:
        actions = "<li class='muted'>No critical gaps</li>"

    # Pipeline
    try:
        deals = pipeline.list_deals(company_id)[:12]
    except Exception:  # noqa: BLE001
        deals = []
    pipe_rows = ""
    for d in deals:
        pipe_rows += (
            f"<tr><td>{_esc(d.get('id'))}</td><td>{_esc(d.get('account'))}</td>"
            f"<td>{_esc(d.get('stage'))}</td><td class='muted'>{_esc(d.get('next_step'))}</td></tr>"
        )
    if not pipe_rows:
        pipe_rows = "<tr><td colspan='4' class='muted'>No deals — add via CLI</td></tr>"

    # Calendar reminders
    try:
        rem = calendar_ops.format_reminders_markdown(company_id, within_days=14)
    except Exception as e:  # noqa: BLE001
        rem = f"Calendar unavailable: {e}"
    rem_html = f"<pre>{_esc(rem[:2000])}</pre>"

    # Grants
    try:
        gmd = grants.format_board_slice(company_id)
    except Exception as e:  # noqa: BLE001
        gmd = f"Grants unavailable: {e}"
    grants_html = f"<pre>{_esc(gmd[:1500])}</pre>"

    # Weekly excerpt
    weekly_text = ""
    wdir = company_dir(company_id) / "weekly"
    if wdir.is_dir():
        files = sorted(wdir.glob("*.md"), reverse=True)
        if files:
            weekly_text = files[0].read_text(encoding="utf-8", errors="replace")[:2000]
    weekly_html = (
        f"<pre>{_esc(weekly_text)}</pre>" if weekly_text else "<p class='muted'>No weekly report yet</p>"
    )

    # Artefact paths (local only)
    cpath = company_dir(company_id)
    artefacts = [
        ("Status", cpath / "status" / "status-latest.md"),
        ("Board pack", cpath / "board-packs" / "board-pack-latest.zip"),
        ("Handoff pack", cpath / "handoff" / "handoff-latest.zip"),
        ("ICS deadlines", cpath / "exports" / "deadlines-latest.ics"),
        ("Pilot offer", cpath / "commercial" / "pilots" / "pilot-offer-latest.zip"),
    ]
    art_rows = ""
    for label, p in artefacts:
        exists = p.is_file()
        art_rows += (
            f"<tr><td>{_esc(label)}</td>"
            f"<td class='{'ok' if exists else 'gap'}'>{'ready' if exists else 'missing'}</td>"
            f"<td class='muted'><code>{_esc(p)}</code></td></tr>"
        )

    body = f"""
    <div class="card">
      <h1>{_esc(company_id)}</h1>
      <p class="score">{_esc(st.get('score'))}/100 <span class="muted">({_esc(st.get('band'))})</span></p>
      <p class="muted">{_esc(st.get('hitl'))}</p>
      <div>
        <form class="inline" method="post" action="/c/{_esc(company_id)}/status">
          <button type="submit">Refresh status</button>
        </form>
        <form class="inline" method="post" action="/c/{_esc(company_id)}/weekly">
          <button class="secondary" type="submit">Weekly board</button>
        </form>
        <form class="inline" method="post" action="/c/{_esc(company_id)}/board">
          <button class="secondary" type="submit">Board pack zip</button>
        </form>
        <form class="inline" method="post" action="/c/{_esc(company_id)}/export">
          <button class="secondary" type="submit">Export reminders</button>
        </form>
      </div>
      <p class="muted" style="margin-top:1rem">Pilot offers, outreach send, and filings stay CLI/human-only.</p>
    </div>
    <div class="grid grid-2">
      <div class="card">
        <h2>Pipeline</h2>
        <table>
          <thead><tr><th>ID</th><th>Account</th><th>Stage</th><th>Next</th></tr></thead>
          <tbody>{pipe_rows}</tbody>
        </table>
      </div>
      <div class="card">
        <h2>Grants</h2>
        {grants_html}
      </div>
    </div>
    <div class="card">
      <h2>Deadline reminders (14d)</h2>
      {rem_html}
    </div>
    <div class="card">
      <h2>Latest weekly excerpt</h2>
      {weekly_html}
    </div>
    <div class="card">
      <h2>Checks</h2>
      <table>
        <thead><tr><th></th><th>Area</th><th>Detail</th></tr></thead>
        <tbody>{checks}</tbody>
      </table>
    </div>
    <div class="card">
      <h2>Next actions</h2>
      <ul>{actions}</ul>
    </div>
    <div class="card">
      <h2>Local artefacts</h2>
      <table>
        <thead><tr><th>Item</th><th>State</th><th>Path</th></tr></thead>
        <tbody>{art_rows}</tbody>
      </table>
      <p><a href="/">← Companies</a></p>
    </div>
    """
    return _layout(company_id, body, flash)


def page_help() -> str:
    body = f"""
    <div class="card">
      <h1>Help</h1>
      <p>This is the <strong>v{_esc(__version__)} local Founder Console</strong> — a thin localhost UI over company memory.</p>
      <ul>
        <li>Binds only to <code>127.0.0.1</code></li>
        <li>Does not expose multi-tenant SaaS</li>
        <li>Does not send email, file IRD/Companies Office, or move money</li>
        <li>For full fleet power use CLI / MCP / Aether skills</li>
      </ul>
      <h2>Desktop-lite</h2>
      <p><code>nz-startup console --open</code> opens your browser. Optional:
      <code>nz-startup desktop</code> uses pywebview if installed.</p>
      <h2>Docs</h2>
      <ul>
        <li><code>RELEASE.md</code></li>
        <li><code>docs/CONSOLE.md</code></li>
        <li><code>docs/GETTING_STARTED.md</code></li>
        <li><code>docs/DEMO.md</code></li>
      </ul>
    </div>
    """
    return _layout("Help", body)


def _page_login(error: str = "") -> str:
    err = f'<p class="gap">{_esc(error)}</p>' if error else ""
    body = f"""
    <div class="card">
      <h1>Console session</h1>
      <p class="muted">Localhost only · session token required (G11)</p>
      {err}
      <form method="POST" action="/login">
        <label>Session token<br/>
          <input name="token" type="password" autocomplete="current-password"
                 style="width:100%;max-width:28rem;padding:.5rem;margin:.5rem 0;border-radius:8px;border:1px solid #334155;background:#0f172a;color:#e5e7eb"/>
        </label>
        <div><button type="submit">Unlock</button></div>
      </form>
      <p class="muted" style="margin-top:1rem">Token printed when the console starts, or set <code>NZ_STARTUP_CONSOLE_TOKEN</code>.</p>
    </div>
    """
    return _layout("Login", body)


class ConsoleHandler(BaseHTTPRequestHandler):
    server_version = f"NZStartupConsole/{__version__}"

    def log_message(self, fmt: str, *args: Any) -> None:
        sys_stderr = __import__("sys").stderr
        sys_stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _token_ok(self, candidate: str) -> bool:
        expected = _expected_token()
        if not expected or not candidate:
            return False
        # T9 — constant-time compare
        return hmac.compare_digest(candidate.encode("utf-8"), expected.encode("utf-8"))

    def _authorized(self) -> bool:
        expected = _expected_token()
        if not expected:
            return True  # auth disabled only if no token configured (should not happen at runtime)
        auth = self.headers.get("Authorization") or ""
        if auth.lower().startswith("bearer ") and self._token_ok(auth[7:].strip()):
            return True
        if self._token_ok((self.headers.get("X-NZ-Startup-Token") or "").strip()):
            return True
        cookies = _parse_cookies(self.headers.get("Cookie") or "")
        if self._token_ok(cookies.get(_COOKIE_NAME) or ""):
            return True
        # one-shot query param for first open from CLI
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        if self._token_ok((qs.get("token") or [""])[0]):
            return True
        return False

    def _send(
        self,
        code: int,
        body: str,
        content_type: str = "text/html; charset=utf-8",
        *,
        set_cookie: str | None = None,
    ) -> None:
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-NZ-Startup-Console", __version__)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        if set_cookie:
            self.send_header(
                "Set-Cookie",
                f"{_COOKIE_NAME}={set_cookie}; Path=/; HttpOnly; SameSite=Strict",
            )
        self.end_headers()
        self.wfile.write(data)

    def _redirect(self, location: str, *, set_cookie: str | None = None) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        if set_cookie:
            self.send_header(
                "Set-Cookie",
                f"{_COOKIE_NAME}={set_cookie}; Path=/; HttpOnly; SameSite=Strict",
            )
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        qs = parse_qs(parsed.query)
        flash = (qs.get("flash") or [""])[0]
        try:
            if path == "/login":
                self._send(200, _page_login())
                return
            if path == "/healthz":
                self._send(200, json.dumps({"ok": True, "version": __version__}), "application/json")
                return
            # Auto-set cookie if token query present and valid
            expected = _expected_token()
            qtok = (qs.get("token") or [""])[0]
            set_ck = qtok if expected and self._token_ok(qtok) else None

            if not self._authorized():
                if path.startswith("/api/"):
                    self._send(401, json.dumps({"error": "unauthorized"}), "application/json")
                    return
                self._send(401, _page_login("Session required"))
                return

            if path == "/":
                self._send(200, page_home(flash), set_cookie=set_ck)
                return
            if path == "/help":
                self._send(200, page_help(), set_cookie=set_ck)
                return
            if path == "/api/companies":
                self._send(
                    200,
                    json.dumps({"companies": _list_companies(), "version": __version__}),
                    "application/json",
                    set_cookie=set_ck,
                )
                return
            if path.startswith("/api/c/") and path.endswith("/status"):
                cid = path.split("/")[3]
                st = status.collect_status(cid)
                self._send(200, json.dumps(st, default=str), "application/json", set_cookie=set_ck)
                return
            if path.startswith("/c/"):
                parts = path.split("/")
                if len(parts) >= 3 and parts[2]:
                    company_id = parts[2]
                    if len(parts) == 3:
                        self._send(200, page_company(company_id, flash), set_cookie=set_ck)
                        return
            self._send(404, _layout("404", "<div class='card'><h1>Not found</h1></div>"))
        except Exception:  # noqa: BLE001
            self._send(
                500,
                _layout(
                    "Error",
                    f"<div class='card'><h1>Error</h1><pre>{_esc(traceback.format_exc())}</pre></div>",
                ),
            )

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        try:
            if path == "/login":
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length).decode("utf-8", errors="replace") if length else ""
                form = parse_qs(raw)
                token = (form.get("token") or [""])[0].strip()
                expected = _expected_token()
                if expected and self._token_ok(token):
                    self._redirect("/?flash=Session+unlocked", set_cookie=token)
                    return
                self._send(401, _page_login("Invalid token"))
                return

            if not self._authorized():
                self._send(401, _page_login("Session required"))
                return

            parts = path.split("/")
            if len(parts) == 4 and parts[1] == "c":
                company_id = parts[2]
                action = parts[3]
                if action == "weekly":
                    weekly.generate_weekly_review(company_id)
                    self._redirect(f"/c/{quote(company_id)}?flash=Weekly+board+generated")
                    return
                if action == "status":
                    status.write_status(company_id)
                    self._redirect(f"/c/{quote(company_id)}?flash=Status+refreshed")
                    return
                if action == "board":
                    board_pack.create_board_pack(company_id, label="console")
                    self._redirect(f"/c/{quote(company_id)}?flash=Board+pack+written")
                    return
                if action == "export":
                    export_reminders.export_all(company_id)
                    self._redirect(f"/c/{quote(company_id)}?flash=Reminders+exported")
                    return
            self._send(404, _layout("404", "<div class='card'><h1>Not found</h1></div>"))
        except Exception as e:  # noqa: BLE001
            msg = quote(str(e)[:100])
            if "/c/" in path:
                cid = path.split("/")[2] if len(path.split("/")) > 2 else ""
                self._redirect(f"/c/{quote(cid)}?flash=Error:+{msg}")
            else:
                self._send(
                    500,
                    _layout("Error", f"<div class='card'><pre>{_esc(traceback.format_exc())}</pre></div>"),
                )


def run_console(
    host: str = "127.0.0.1",
    port: int = 8765,
    *,
    open_browser: bool = False,
    token: str | None = None,
) -> None:
    global _CONSOLE_TOKEN
    if host not in ("127.0.0.1", "localhost", "::1"):
        raise ValueError(
            "Console must bind to localhost only (127.0.0.1). "
            "Refusing non-local bind — this is not a multi-tenant server."
        )
    # G11 — always mint a session token unless env already set
    _CONSOLE_TOKEN = (token or os.environ.get("NZ_STARTUP_CONSOLE_TOKEN") or "").strip()
    if not _CONSOLE_TOKEN:
        _CONSOLE_TOKEN = secrets.token_urlsafe(24)
    companies_dir().mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((host, port), ConsoleHandler)
    url = f"http://{host}:{port}/?token={_CONSOLE_TOKEN}"
    print(f"NZ Start-Up Console v{__version__}")
    print(f"Open {url}")
    print(f"Session token: {_CONSOLE_TOKEN}")
    print("Localhost only · Ctrl+C to stop · HITL: no send/file/pay from this UI.")
    if open_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nConsole stopped.")
        httpd.server_close()


def run_desktop(port: int = 8765, *, token: str | None = None) -> None:
    """
    Desktop-lite: prefer pywebview window; fall back to browser console.
    Still localhost-only + session token.
    """
    global _CONSOLE_TOKEN
    host = "127.0.0.1"
    _CONSOLE_TOKEN = (token or os.environ.get("NZ_STARTUP_CONSOLE_TOKEN") or "").strip()
    if not _CONSOLE_TOKEN:
        _CONSOLE_TOKEN = secrets.token_urlsafe(24)
    companies_dir().mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((host, port), ConsoleHandler)
    url = f"http://{host}:{port}/?token={_CONSOLE_TOKEN}"
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    print(f"NZ Start-Up Desktop-lite v{__version__} → {url}")
    print(f"Session token: {_CONSOLE_TOKEN}")
    try:
        import webview  # type: ignore

        webview.create_window(
            f"NZ Start-Up Console v{__version__}",
            url,
            width=1100,
            height=800,
        )
        webview.start()
    except ImportError:
        print("pywebview not installed — opening system browser.")
        print("Optional: pip install pywebview")
        webbrowser.open(url)
        try:
            thread.join()
        except KeyboardInterrupt:
            pass
    finally:
        httpd.shutdown()
