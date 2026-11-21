#!/usr/bin/env python3
"""Generate a self-contained SVG animation from GitHub contribution *levels*.

Uses the built-in workflow GITHUB_TOKEN and Python standard library.
No private repo names, commits, messages, or raw data are embedded in SVG.
"""
import datetime as dt
import html
import json
import os
from pathlib import Path
import urllib.request

USERNAME = os.environ.get("GITHUB_USERNAME", "Jad-RAMOSS")
TOKEN = os.environ.get("GITHUB_TOKEN")
OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "contribution-signal.svg"
COLORS = {
    "NONE": "#183040",
    "FIRST_QUARTILE": "#1B5E63",
    "SECOND_QUARTILE": "#20847D",
    "THIRD_QUARTILE": "#28B299",
    "FOURTH_QUARTILE": "#65E7BB",
}


def fetch_weeks():
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN is required — cannot invent contribution history")
    query = '''query($login:String!){user(login:$login){contributionsCollection{
      contributionCalendar{weeks{contributionDays{date contributionLevel}}}
    }}}'''
    payload = json.dumps({"query": query, "variables": {"login": USERNAME}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=payload,
        headers={"Authorization": f"Bearer {TOKEN}",
                 "Content-Type": "application/json",
                 "User-Agent": "profile-contribution-signal"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.load(response)
    if data.get("errors"):
        raise RuntimeError(f"GitHub GraphQL request failed: {data['errors']}")
    user = (data.get("data") or {}).get("user")
    if not user:
        raise RuntimeError(f"GitHub account {USERNAME!r} was not found")
    return user["contributionsCollection"]["contributionCalendar"]["weeks"]


def make_svg(weeks):
    # GitHub returns a week-by-week grid; days in a week are calendar dates.
    cell, gap, x0, y0 = 10, 4, 20, 57
    step = cell + gap
    width = max(760, x0 * 2 + len(weeks) * step)
    height = 186
    tiles = []
    active = []
    for col, week in enumerate(weeks):
        for day in week["contributionDays"]:
            date = dt.date.fromisoformat(day["date"])
            row = (date.weekday() + 1) % 7  # Sunday-first calendar
            x, y = x0 + col * step, y0 + row * step
            level = day["contributionLevel"]
            if level not in COLORS:
                raise ValueError(f"Unexpected GitHub level: {level}")
            tiles.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                f'rx="2.5" fill="{COLORS[level]}">'
                f'<title>{date.isoformat()} · activity: {level.lower().replace("_", " ")}</title></rect>'
            )
            if level != "NONE":
                active.append((date, x + cell / 2, y + cell / 2))
    # Pulse travels through the last active days, not a copied "snake" game.
    recent = sorted(active, key=lambda a: a[0])[-28:]
    path = "M " + " L ".join(f"{x:.1f} {y:.1f}" for _, x, y in recent) if len(recent) > 1 else ""
    motion = ""
    if path:
        motion = (
            f'<path d="{path}" fill="none" stroke="#F39A67" '
            f'stroke-width="2.3" stroke-linejoin="round" opacity=".45"/>'
            f'<circle r="8" fill="#F7A86D" opacity=".20"><animateMotion '
            f'dur="13s" repeatCount="indefinite" path="{path}"/></circle>'
            f'<circle r="4.5" fill="#FFBD82"><animateMotion '
            f'dur="13s" repeatCount="indefinite" path="{path}"/></circle>'
        )
        endpoint = f'<circle cx="{recent[-1][1]:.1f}" cy="{recent[-1][2]:.1f}" r="3" fill="#FFBD82"/>'
    else:
        endpoint = ''
    label = html.escape(USERNAME, quote=True)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{label} GitHub activity levels">
<title>Signal Path · {label}'s GitHub activity</title>
<desc>Activity levels from GitHub's contribution calendar. Animated route across recent active days. No repository names or commit details.</desc>
<defs>
 <linearGradient id="background" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#091623"/><stop offset="1" stop-color="#152E3C"/></linearGradient>
</defs>
<rect width="{width}" height="{height}" rx="15" fill="url(#background)"/>
<text x="20" y="28" font-family="Arial,Helvetica,sans-serif" font-weight="bold" font-size="14" letter-spacing="2" fill="#8BF4D5">SIGNAL PATH</text>
<text x="{width-20}" y="28" text-anchor="end" font-family="Arial,Helvetica,sans-serif" font-size="11" fill="#91ABB9">LIVE ACTIVITY LEVELS</text>
{''.join(tiles)}
{motion}
{endpoint}
<text x="20" y="{height-14}" font-family="Arial,Helvetica,sans-serif" font-size="11" fill="#9AB5C2">GitHub contribution calendar · Updated automatically</text>
<circle cx="{width-89}" cy="{height-18}" r="4" fill="#F6A16F"/><text x="{width-78}" y="{height-14}" font-family="Arial,Helvetica,sans-serif" font-size="10" fill="#9AB5C2">SIGNAL</text>
</svg>'''


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(make_svg(fetch_weeks()), encoding="utf-8")
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
