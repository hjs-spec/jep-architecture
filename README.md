# JEP Architecture

Developer-oriented architecture notes and diagrams for the JEP / HJS / JAC accountability runtime stack.

This repository intentionally uses only Markdown and Mermaid so the architecture can be read in code review, rendered by GitHub, and copied into implementation docs without a documentation framework.

## What this stack describes

JEP defines how an agent action is packaged for accountability. HJS carries the signed/hardened job state that JEP middleware exchanges. JAC provides the canonical archive and replay contract. Runtime components execute tools through those layers, while SDKs and integrations make the same accountability path available to applications.

## Diagram index

| Diagram | Purpose | Markdown | SVG |
| --- | --- | --- | --- |
| Protocol Stack | Shows how JEP, HJS, JAC, runtime, SDKs, and integrations depend on each other. | [diagrams/protocol-stack.md](diagrams/protocol-stack.md) | [diagrams/protocol-stack.svg](diagrams/protocol-stack.svg) |
| Execution Path | Shows the path a runtime action takes from agent request to replayable archive. | [diagrams/execution-path.md](diagrams/execution-path.md) | [diagrams/execution-path.svg](diagrams/execution-path.svg) |
| Delegation Lineage | Shows how human intent is delegated through agents and tools to external systems. | [diagrams/delegation-lineage.md](diagrams/delegation-lineage.md) | [diagrams/delegation-lineage.svg](diagrams/delegation-lineage.svg) |
| Replay Verification | Shows how archived records are verified before replay output is trusted. | [diagrams/replay-verification.md](diagrams/replay-verification.md) | [diagrams/replay-verification.svg](diagrams/replay-verification.svg) |
| Trust Boundary | Shows which principals own decisions, execution, policy, tool contracts, and outside effects. | [diagrams/trust-boundary.md](diagrams/trust-boundary.md) | [diagrams/trust-boundary.svg](diagrams/trust-boundary.svg) |

## How to read the diagrams

Start with the [Protocol Stack](diagrams/protocol-stack.md) to understand the layer boundaries. Then read the [Execution Path](diagrams/execution-path.md) to see which components touch a request. The [Delegation Lineage](diagrams/delegation-lineage.md), [Replay Verification](diagrams/replay-verification.md), and [Trust Boundary](diagrams/trust-boundary.md) diagrams fill in the audit, replay, and security concerns that developers need while implementing middleware, SDKs, or integrations.

See [architecture-notes.md](architecture-notes.md) for implementation notes, data responsibilities, and development guidance.

## Regenerating SVG diagrams

The Mermaid blocks in `diagrams/*.md` are the source of truth. Checked-in SVG files are included as lightweight previews for tools that do not render Mermaid directly.

Regenerate the checked-in SVG previews without external dependencies:

```bash
python scripts/generate-static-svgs.py
```

If your local environment can install Mermaid CLI, you can also render directly from the Markdown Mermaid blocks with `mmdc`. Some restricted CI or registry environments may block `npx @mermaid-js/mermaid-cli`; that does not block maintaining this repository because the dependency-free generator above is the supported repo-local path.
