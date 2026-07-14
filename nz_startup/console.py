"""
Local Founder Console — localhost-only dashboard (v1.0).

Not multi-tenant SaaS. Binds to 127.0.0.1 only.
Never sends email, files government forms, or moves money.
"""
from __future__ import annotations

import html
import json
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from nz_startup import __version__, memory, status, weekly
from nz_startup.paths import companies_dir


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
    main {{ max-width: 960px; margin: 0 auto; padding: 1.5rem; }}
    .card {{
      background: color-mix(in srgb, var(--card) 92%, transparent);
      border: 1px solid var(--line); border-radius: 14px; padding: 1.25rem; margin-bottom: 1rem;
      backdrop-filter: blur(8px);
    }}
    h1,h2 {{ margin: 0 0 .75rem; }}
    .muted {{ color: var(--muted); }}
    .score {{ font-size: 2rem; font-weight: 700; color: var(--accent); }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ text-align: left; padding: .5rem .4rem; border-bottom: 1px solid var(--line); }}
    .ok {{ color: var(--ok); }} .gap {{ color: var(--bad); }}
    form.inline {{ display: inline; }}
    button, .btn {{
      background: #0369a1; color: white; border: 0; border-radius: 8px;
      padding: .45rem .8rem; cursor: pointer; font-weight: 600;
    }}
    button.secondary {{ background: #334155; }}
    .flash {{
      background: #14532d55; border: 1px solid #22c55e66; padding: .75rem 1rem;
      border-radius: 10px; margin-bottom: 1rem;
    }}
    code {{ background: #0f172a; padding: .1rem .35rem; border-radius: 4px; }}
    ul {{ padding-left: 1.2rem; }}
    footer {{ max-width: 960px; margin: 2rem auto; padding: 0 1.5rem 2rem; color: var(--muted); font-size: .9rem; }}
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


def page_home(flash: str = "") -> str:
    companies = _list_companies()
    rows = ""
    if not companies:
        rows = "<tr><td colspan='3' class='muted'>No companies yet. Run <code>nz-startup onboard my-co</code></td></tr>"
    else:
        for c in companies:
            rows += (
                f"<tr><td><a href='/c/{_esc(c)}'>{_esc(c)}</a></td>"
                f"<td><a class='btn' href='/c/{_esc(c)}'>Open</a></td>"
                f"<td>"
                f"<form class='inline' method='post' action='/c/{_esc(c)}/weekly'>"
                f"<button type='submit'>Weekly</button></form> "
                f"<form class='inline' method='post' action='/c/{_esc(c)}/status'>"
                f"<button class='secondary' type='submit'>Refresh status</button></form>"
                f"</td></tr>"
            )
    body = f"""
    <div class="card">
      <h1>Founder companies</h1>
      <p class="muted">Local memory under <code>memory/companies/</code>. Not multi-tenant SaaS.</p>
      <table>
        <thead><tr><th>Company id</th><th></th><th>Actions</th></tr></thead>
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
    snap = st.get("snapshot") or {}
    snap_rows = "".join(
        f"<tr><td>{_esc(k.replace('_', ' '))}</td><td>{_esc(v)}</td></tr>"
        for k, v in snap.items()
    )
    body = f"""
    <div class="card">
      <h1>{_esc(company_id)}</h1>
      <p class="score">{_esc(st.get('score'))}/100 <span class="muted">({_esc(st.get('band'))})</span></p>
      <p class="muted">{_esc(st.get('hitl'))}</p>
      <form class="inline" method="post" action="/c/{_esc(company_id)}/status">
        <button type="submit">Refresh status</button>
      </form>
      <form class="inline" method="post" action="/c/{_esc(company_id)}/weekly">
        <button class="secondary" type="submit">Generate weekly board</button>
      </form>
      <p class="muted" style="margin-top:1rem">Board/handoff/pilot packs stay CLI-only (safer HITL surface).</p>
    </div>
    <div class="card">
      <h2>Snapshot</h2>
      <table><tbody>{snap_rows}</tbody></table>
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
      <p><a href="/">← Companies</a></p>
    </div>
    """
    return _layout(company_id, body, flash)


def page_help() -> str:
    body = """
    <div class="card">
      <h1>Help</h1>
      <p>This is the <strong>v1.0 local Founder Console</strong> — a thin localhost UI over company memory.</p>
      <ul>
        <li>Binds only to <code>127.0.0.1</code></li>
        <li>Does not expose multi-tenant SaaS</li>
        <li>Does not send email, file IRD/Companies Office, or move money</li>
        <li>For full fleet power use CLI / MCP / Aether skills</li>
      </ul>
      <h2>Related docs</h2>
      <ul>
        <li><code>docs/GETTING_STARTED.md</code></li>
        <li><code>docs/DEMO.md</code></li>
        <li><code>docs/WHITE_LABEL.md</code></li>
        <li><code>RELEASE.md</code></li>
      </ul>
    </div>
    """
    return _layout("Help", body)


class ConsoleHandler(BaseHTTPRequestHandler):
    server_version = f"NZStartupConsole/{__version__}"

    def log_message(self, fmt: str, *args: Any) -> None:
        # quieter default
        sys_stderr = __import__("sys").stderr
        sys_stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send(self, code: int, body: str, content_type: str = "text/html; charset=utf-8") -> None:
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-NZ-Startup-Console", __version__)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _redirect(self, location: str) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        qs = parse_qs(parsed.query)
        flash = (qs.get("flash") or [""])[0]
        try:
            if path == "/":
                self._send(200, page_home(flash))
                return
            if path == "/help":
                self._send(200, page_help())
                return
            if path == "/api/companies":
                self._send(
                    200,
                    json.dumps({"companies": _list_companies(), "version": __version__}),
                    "application/json",
                )
                return
            if path.startswith("/c/"):
                parts = path.split("/")
                # /c/{id} or /c/{id}/...
                if len(parts) >= 3 and parts[2]:
                    company_id = parts[2]
                    if len(parts) == 3:
                        self._send(200, page_company(company_id, flash))
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
            parts = path.split("/")
            # /c/{id}/weekly or /c/{id}/status
            if len(parts) == 4 and parts[1] == "c":
                company_id = parts[2]
                action = parts[3]
                if action == "weekly":
                    weekly.generate_weekly_review(company_id)
                    self._redirect(f"/c/{company_id}?flash=Weekly+board+generated")
                    return
                if action == "status":
                    status.write_status(company_id)
                    self._redirect(f"/c/{company_id}?flash=Status+refreshed")
                    return
            self._send(404, _layout("404", "<div class='card'><h1>Not found</h1></div>"))
        except Exception as e:  # noqa: BLE001
            msg = str(e).replace(" ", "+")[:120]
            if "/c/" in path:
                cid = path.split("/")[2] if len(path.split("/")) > 2 else ""
                self._redirect(f"/c/{cid}?flash=Error:+{_esc(msg)}")
            else:
                self._send(
                    500,
                    _layout("Error", f"<div class='card'><pre>{_esc(traceback.format_exc())}</pre></div>"),
                )


def run_console(host: str = "127.0.0.1", port: int = 8765) -> None:
    if host not in ("127.0.0.1", "localhost", "::1"):
        raise ValueError(
            "Console must bind to localhost only (127.0.0.1). "
            "Refusing non-local bind — this is not a multi-tenant server."
        )
    # Ensure companies dir exists
    companies_dir().mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((host, port), ConsoleHandler)
    print(f"NZ Start-Up Console v{__version__}")
    print(f"Open http://{host}:{port}/  (localhost only)")
    print("Ctrl+C to stop. HITL: no send/file/pay from this UI.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nConsole stopped.")
        httpd.server_close()
