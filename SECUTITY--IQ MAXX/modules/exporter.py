#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IQ MAXX (by dk) - Data & Security Audit Exporter
Formats: HTML Dashboard (Dark Cyber Blue & Green), JSON, CSV
"""

import json
import csv
import os
import datetime
from typing import List, Dict, Any

class Exporter:
    """Exports Wi-Fi credentials and audit results into various shareable formats."""

    @staticmethod
    def export_json(data: List[Dict[str, Any]], filepath: str) -> bool:
        try:
            payload = {
                "tool": "IQ MAXX (by dk)",
                "version": "2.5.0",
                "generated_at": datetime.datetime.now().isoformat(),
                "total_profiles": len(data),
                "networks": data
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting JSON: {e}")
            return False

    @staticmethod
    def export_csv(data: List[Dict[str, Any]], filepath: str) -> bool:
        try:
            if not data:
                return False
            fieldnames = ["ssid", "password", "auth", "cipher", "platform"]
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                for item in data:
                    writer.writerow(item)
            return True
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return False

    @staticmethod
    def export_html(data: List[Dict[str, Any]], filepath: str) -> bool:
        """Generates a stunning Cyberpunk Blue & Neon Green interactive HTML report."""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total = len(data)
            open_count = sum(1 for d in data if "open" in str(d.get("password", "")).lower() or "open" in str(d.get("auth", "")).lower())
            secured_count = total - open_count

            rows_html = ""
            for idx, item in enumerate(data, 1):
                ssid = str(item.get("ssid", "Unknown"))
                pwd = str(item.get("password", ""))
                auth = str(item.get("auth", "Unknown"))
                cipher = str(item.get("cipher", "Unknown"))
                plat = str(item.get("platform", "Unknown"))

                is_open = "open" in pwd.lower() or "open" in auth.lower()
                badge_class = "badge-open" if is_open else "badge-secure"
                badge_text = "OPEN / NO PWD" if is_open else "PROTECTED"

                # Calculate strength estimate
                pwd_len = len(pwd)
                if is_open:
                    str_badge = '<span class="pill pill-danger">UNSECURED</span>'
                elif pwd.startswith("["):
                    str_badge = '<span class="pill pill-info">SYSTEM PROTECTED</span>'
                elif pwd_len >= 12:
                    str_badge = '<span class="pill pill-success">STRONG (12+ chars)</span>'
                elif pwd_len >= 8:
                    str_badge = '<span class="pill pill-warning">MODERATE</span>'
                else:
                    str_badge = '<span class="pill pill-danger">WEAK (&lt;8 chars)</span>'

                rows_html += f"""
                <tr class="table-row">
                    <td class="idx-col">{idx}</td>
                    <td class="ssid-col"><strong>{ssid}</strong></td>
                    <td class="pwd-col">
                        <div class="pwd-container">
                            <span class="pwd-text" id="pwd-{idx}">{pwd}</span>
                            <button class="copy-btn" onclick="copyText('pwd-{idx}', this)" title="Copy Password">📋</button>
                        </div>
                    </td>
                    <td><span class="badge {badge_class}">{badge_text}</span></td>
                    <td>{str_badge}</td>
                    <td><span class="cipher-tag">{auth}</span> <small class="text-dim">({cipher})</small></td>
                    <td><span class="platform-tag">{plat}</span></td>
                </tr>
                """

            html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IQ MAXX (by dk) - Wi-Fi Audit Report</title>
    <style>
        :root {{
            --bg-primary: #0a0e17;
            --bg-secondary: #111927;
            --bg-card: #152238;
            --border-color: #1e3352;
            --neon-blue: #00d2ff;
            --electric-blue: #3a7bd5;
            --neon-green: #00ff88;
            --mint-green: #10b981;
            --amber-warn: #f59e0b;
            --danger-red: #ef4444;
            --text-main: #f3f4f6;
            --text-dim: #9ca3af;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }}
        body {{
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            padding: 2rem 1rem;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            background: linear-gradient(135deg, rgba(16, 25, 44, 0.9) 0%, rgba(10, 14, 23, 0.95) 100%);
            border: 1px solid var(--border-color);
            border-top: 4px solid var(--neon-blue);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0, 210, 255, 0.1);
            position: relative;
            overflow: hidden;
        }}
        header::after {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 300px;
            height: 100%;
            background: radial-gradient(circle, rgba(0, 255, 136, 0.15) 0%, transparent 70%);
            pointer-events: none;
        }}
        .brand-title {{
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: 1px;
            background: linear-gradient(90deg, var(--neon-blue), var(--neon-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }}
        .brand-subtitle {{
            color: var(--neon-green);
            font-size: 1rem;
            font-style: italic;
            margin-left: 0.5rem;
            font-weight: 400;
        }}
        .tagline {{
            color: var(--text-dim);
            margin-top: 0.5rem;
            font-size: 0.95rem;
        }}
        .meta-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 1.5rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
            flex-wrap: wrap;
            gap: 1rem;
        }}
        .timestamp {{
            color: var(--text-dim);
            font-size: 0.85rem;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2rem;
        }}
        .stat-card {{
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.25rem;
            position: relative;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .stat-card:hover {{
            transform: translateY(-3px);
            border-color: var(--neon-blue);
        }}
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--neon-blue);
        }}
        .stat-label {{
            color: var(--text-dim);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 0.25rem;
        }}
        .table-container {{
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }}
        .table-header-bar {{
            padding: 1.25rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            flex-wrap: wrap;
            gap: 1rem;
        }}
        .search-input {{
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.6rem 1rem;
            color: var(--text-main);
            outline: none;
            width: 280px;
            transition: border-color 0.2s;
        }}
        .search-input:focus {{
            border-color: var(--neon-blue);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}
        th {{
            background-color: var(--bg-card);
            color: var(--neon-blue);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 1rem;
            font-weight: 600;
        }}
        td {{
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
            font-size: 0.95rem;
        }}
        tr:hover td {{
            background-color: rgba(0, 210, 255, 0.03);
        }}
        .idx-col {{
            color: var(--text-dim);
            font-weight: 600;
            width: 50px;
        }}
        .ssid-col {{
            color: #ffffff;
        }}
        .pwd-container {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-family: 'Consolas', monospace;
            background-color: var(--bg-primary);
            padding: 0.35rem 0.6rem;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.05);
            width: fit-content;
        }}
        .pwd-text {{
            color: var(--neon-green);
        }}
        .copy-btn {{
            background: none;
            border: none;
            cursor: pointer;
            font-size: 0.9rem;
            opacity: 0.6;
            transition: opacity 0.2s;
        }}
        .copy-btn:hover {{
            opacity: 1.0;
        }}
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.6rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        .badge-secure {{
            background-color: rgba(16, 185, 129, 0.15);
            color: var(--neon-green);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}
        .badge-open {{
            background-color: rgba(239, 68, 68, 0.15);
            color: var(--danger-red);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}
        .pill {{
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .pill-success {{ background: rgba(0, 255, 136, 0.15); color: var(--neon-green); }}
        .pill-warning {{ background: rgba(245, 158, 11, 0.15); color: var(--amber-warn); }}
        .pill-danger  {{ background: rgba(239, 68, 68, 0.15); color: var(--danger-red); }}
        .pill-info    {{ background: rgba(0, 210, 255, 0.15); color: var(--neon-blue); }}
        .cipher-tag {{
            color: var(--neon-blue);
            font-size: 0.85rem;
        }}
        .platform-tag {{
            background-color: var(--bg-card);
            color: var(--text-dim);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }}
        footer {{
            text-align: center;
            margin-top: 3rem;
            color: var(--text-dim);
            font-size: 0.85rem;
        }}
        footer a {{
            color: var(--neon-blue);
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1 class="brand-title">IQ MAXX</h1>
                <span class="brand-subtitle">(by dk)</span>
            </div>
            <p class="tagline">Wireless Security Audit & Saved Credentials Intelligence Dashboard</p>
            <div class="meta-bar">
                <span class="timestamp">Generated: <strong>{timestamp}</strong></span>
                <span class="timestamp">Target Platform: <strong>Cross-Platform</strong></span>
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{total}</div>
                <div class="stat-label">Total Networks Audited</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: var(--neon-green);">{secured_count}</div>
                <div class="stat-label">Secured Networks (WPA2/WPA3)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: var(--danger-red);">{open_count}</div>
                <div class="stat-label">Open / Unsecured Networks</div>
            </div>
        </div>

        <div class="table-container">
            <div class="table-header-bar">
                <h3>Extracted Credentials ({total})</h3>
                <input type="text" id="searchInput" class="search-input" placeholder="Search SSID, Auth, Platform..." onkeyup="filterTable()">
            </div>
            <table id="credTable">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>SSID Name</th>
                        <th>Extracted Passphrase</th>
                        <th>Status</th>
                        <th>Security Rating</th>
                        <th>Authentication / Cipher</th>
                        <th>Source Platform</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <footer>
            <p>Generated by <strong>IQ MAXX (by dk)</strong> • For security auditing & authorized credential recovery.</p>
        </footer>
    </div>

    <script>
        function filterTable() {{
            const input = document.getElementById('searchInput').value.toLowerCase();
            const rows = document.querySelectorAll('#credTable tbody tr');
            rows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(input) ? '' : 'none';
            }});
        }}

        function copyText(elementId, btn) {{
            const el = document.getElementById(elementId);
            if (!el) return;
            const text = el.innerText;
            navigator.clipboard.writeText(text).then(() => {{
                const orig = btn.innerText;
                btn.innerText = '✅';
                setTimeout(() => {{ btn.innerText = orig; }}, 1500);
            }});
        }}
    </script>
</body>
</html>
"""
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_template)
            return True
        except Exception as e:
            print(f"Error exporting HTML: {e}")
            return False
