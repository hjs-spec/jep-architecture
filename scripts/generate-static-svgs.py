#!/usr/bin/env python3
"""Generate dependency-free SVG renderings for the architecture diagrams.

The authoritative diagrams are the Mermaid blocks in diagrams/*.md. This script
keeps checked-in SVG previews available in environments where Mermaid CLI cannot
be installed from npm.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIAGRAM_DIR = ROOT / "diagrams"


@dataclass(frozen=True)
class Box:
    x: int
    y: int
    width: int
    height: int
    style: str
    lines: tuple[str, ...]


def svg_header(width: int, height: int, title: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">Static SVG preview generated from the repository architecture diagram definitions.</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#394150" />
    </marker>
    <style>
      .title {{ font: 700 22px Arial, sans-serif; fill: #172033; }}
      .box {{ rx: 12; ry: 12; stroke-width: 1.7; }}
      .protocol {{ fill: #e8f1ff; stroke: #2f6fed; }}
      .runtime {{ fill: #edf8f0; stroke: #2c8a4a; }}
      .archive {{ fill: #fff7e6; stroke: #d99000; }}
      .external {{ fill: #fff0f0; stroke: #d64545; }}
      .label {{ font: 700 15px Arial, sans-serif; fill: #172033; }}
      .small {{ font: 12px Arial, sans-serif; fill: #394150; }}
      .edge {{ stroke: #394150; stroke-width: 1.6; fill: none; marker-end: url(#arrow); }}
      .dash {{ stroke-dasharray: 6 5; }}
    </style>
  </defs>
'''


def text_block(x: float, y: float, lines: tuple[str, ...], anchor: str = "middle") -> str:
    output: list[str] = []
    for index, line in enumerate(lines):
        css_class = "label" if index == 0 else "small"
        output.append(
            f'  <text x="{x}" y="{y + index * 18}" text-anchor="{anchor}" class="{css_class}">{escape(line)}</text>'
        )
    return "\n".join(output) + "\n"


def box(item: Box) -> str:
    center_x = item.x + item.width / 2
    return (
        f'  <rect x="{item.x}" y="{item.y}" width="{item.width}" height="{item.height}" class="box {item.style}" />\n'
        + text_block(center_x, item.y + 28, item.lines)
    )


def arrow(x1: float, y1: float, x2: float, y2: float, label: str | None = None, dashed: bool = False) -> str:
    css_class = "edge dash" if dashed else "edge"
    output = f'  <path d="M {x1} {y1} L {x2} {y2}" class="{css_class}" />\n'
    if label:
        output += f'  <text x="{(x1 + x2) / 2}" y="{(y1 + y2) / 2 - 8}" text-anchor="middle" class="small">{escape(label)}</text>\n'
    return output


def write_svg(name: str, content: str) -> None:
    (DIAGRAM_DIR / name).write_text(content + "</svg>\n", encoding="utf-8")


def protocol_stack() -> None:
    width, height = 980, 620
    content = svg_header(width, height, "Protocol Stack Diagram")
    content += '  <text x="490" y="38" text-anchor="middle" class="title">Protocol Stack: JEP → HJS → JAC → Runtime → SDKs → Integrations</text>\n'
    items = [
        ("JEP", "Job Envelope Protocol", "action envelope, actor metadata", "protocol"),
        ("HJS", "Hardened Job State", "signed state, policy claims", "protocol"),
        ("JAC", "Job Accountability Canon", "canonical archive, replay contract", "protocol"),
        ("Runtime", "agent loop, middleware hooks", "tool dispatcher", "runtime"),
        ("SDKs", "typed builders, validators", "replay clients", "archive"),
        ("Integrations", "tools, APIs", "workflow systems", "archive"),
    ]
    x, y, box_width, box_height = 350, 75, 280, 72
    for index, (name, detail, note, style) in enumerate(items):
        current_y = y + index * 88
        content += box(Box(x, current_y, box_width, box_height, style, (name, detail, note)))
        if index < len(items) - 1:
            content += arrow(x + box_width / 2, current_y + box_height, x + box_width / 2, current_y + 88, "depends on")
    write_svg("protocol-stack.svg", content)


def execution_path() -> None:
    width, height = 1120, 350
    content = svg_header(width, height, "Execution Path Diagram")
    content += '  <text x="560" y="38" text-anchor="middle" class="title">Execution Path: Agent Runtime → JEP Middleware → Tool Execution → Archive → Replay</text>\n'
    items = [
        ("Agent Runtime", "receives task + context", "runtime"),
        ("JEP Middleware", "creates envelope", "protocol"),
        ("Tool Execution", "validates HJS, runs tool", "runtime"),
        ("Archive", "writes JAC record", "archive"),
        ("Replay", "reconstructs path", "archive"),
    ]
    x0, y, box_width, box_height, gap = 40, 115, 180, 82, 50
    for index, (name, detail, style) in enumerate(items):
        current_x = x0 + index * (box_width + gap)
        content += box(Box(current_x, y, box_width, box_height, style, (name, detail)))
        if index < len(items) - 1:
            content += arrow(current_x + box_width, y + box_height / 2, current_x + box_width + gap - 6, y + box_height / 2)
    content += f'  <path d="M {x0 + 4 * (box_width + gap) + box_width / 2} {y + box_height} C 780 310, 260 310, {x0 + box_width / 2} {y + box_height}" class="edge dash" />\n'
    content += '  <text x="560" y="300" text-anchor="middle" class="small">debug / verify / reproduce from replay back into runtime investigation</text>\n'
    write_svg("execution-path.svg", content)


def delegation_lineage() -> None:
    width, height = 1120, 380
    content = svg_header(width, height, "Delegation Lineage Diagram")
    content += '  <text x="560" y="38" text-anchor="middle" class="title">Delegation Lineage: Human → Agent → Sub-Agent → Tool → External System</text>\n'
    items = [
        ("Human", "intent + approval", "protocol"),
        ("Agent", "plans work", "protocol"),
        ("Sub-Agent", "bounded task", "protocol"),
        ("Tool", "typed capability", "runtime"),
        ("External System", "third-party side effect", "external"),
    ]
    y = 125
    for index, (name, detail, style) in enumerate(items):
        current_x = 45 + index * 215
        content += box(Box(current_x, y, 165, 82, style, (name, detail)))
        if index < len(items) - 1:
            content += arrow(current_x + 165, y + 35, current_x + 210, y + 35, "delegates" if index < 3 else "calls")
        if index > 0:
            content += arrow(current_x, y + 65, current_x - 45, y + 65, "evidence")
    write_svg("delegation-lineage.svg", content)


def replay_verification() -> None:
    width, height = 1120, 380
    content = svg_header(width, height, "Replay Verification Diagram")
    content += '  <text x="560" y="38" text-anchor="middle" class="title">Replay Verification: Archive → Canonicalization → Hash Verification → Lineage Verification → Result</text>\n'
    items = [
        ("Archive", "JAC records", "archive"),
        ("Canonicalization", "stable encoding", "protocol"),
        ("Hash Verification", "digests + signatures", "protocol"),
        ("Lineage Verification", "delegation + policy", "protocol"),
        ("Result", "verified?", "archive"),
    ]
    y = 115
    for index, (name, detail, style) in enumerate(items):
        current_x = 35 + index * 205
        content += box(Box(current_x, y, 165, 82, style, (name, detail)))
        if index < len(items) - 1:
            content += arrow(current_x + 165, y + 41, current_x + 200, y + 41)
    content += box(Box(830, 250, 130, 65, "runtime", ("Accept Replay", "verified trace")))
    content += box(Box(975, 250, 130, 65, "external", ("Reject Replay", "mismatch report")))
    content += arrow(937, 197, 895, 250, "yes")
    content += arrow(995, 197, 1040, 250, "no")
    write_svg("replay-verification.svg", content)


def trust_boundary() -> None:
    width, height = 1060, 670
    content = svg_header(width, height, "Trust Boundary Diagram")
    content += '  <text x="530" y="38" text-anchor="middle" class="title">Trust Boundary: Human / Agent / Organization / Tool / External System</text>\n'
    boundaries = [
        (35, 75, 210, 140, "protocol", "Human trust boundary"),
        (300, 75, 210, 140, "runtime", "Agent trust boundary"),
        (575, 75, 430, 215, "archive", "Organization trust boundary"),
        (300, 360, 210, 140, "runtime", "Tool trust boundary"),
        (575, 360, 430, 140, "external", "External system trust boundary"),
    ]
    for x, y, width, height, style, label in boundaries:
        content += f'  <rect x="{x}" y="{y}" width="{width}" height="{height}" class="box {style}" opacity="0.45" />\n'
        content += f'  <text x="{x + 12}" y="{y + 24}" class="label">{escape(label)}</text>\n'
    content += box(Box(70, 125, 140, 64, "protocol", ("Human", "intent owner")))
    content += box(Box(335, 125, 140, 64, "runtime", ("Agent", "planner")))
    content += box(Box(615, 125, 155, 64, "archive", ("Policy", "permissions")))
    content += box(Box(810, 190, 155, 64, "archive", ("Archive", "audit records")))
    content += box(Box(335, 410, 140, 64, "runtime", ("Tool", "capability")))
    content += box(Box(690, 410, 180, 64, "external", ("External System", "API / files")))
    content += arrow(210, 157, 335, 157, "intent")
    content += arrow(475, 145, 615, 145, "policy check")
    content += arrow(690, 189, 405, 410, "allowed scope")
    content += arrow(405, 189, 405, 410, "JEP + HJS")
    content += arrow(475, 442, 690, 442, "side effect")
    content += arrow(870, 458, 810, 240, "response evidence")
    content += arrow(475, 430, 810, 230, "tool evidence")
    content += arrow(405, 189, 810, 215, "decision trace")
    content += arrow(810, 215, 210, 157, "audit / replay")
    write_svg("trust-boundary.svg", content)


def main() -> None:
    DIAGRAM_DIR.mkdir(exist_ok=True)
    protocol_stack()
    execution_path()
    delegation_lineage()
    replay_verification()
    trust_boundary()


if __name__ == "__main__":
    main()
