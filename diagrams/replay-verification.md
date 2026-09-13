# Scoped verification result

```mermaid
flowchart TB
    Archive["Archive with explicit format"]
    Core["Core syntax and signature checks"]
    Result["Actual Level 1 result and diagnostics"]
    Extra["Optional higher-scope validators"]
    Report["Combined report with unresolved checks"]
    Archive -->|preserve signed members| Core
    Core -->|report performed checks| Result
    Result -->|report Core outcome| Report
    Archive -->|supply extra evidence| Extra
    Extra -->|report supported scopes| Report
```

Core canonicalization and trusted-key signature verification follow JEP rules. The current reference API returns Level 1; it does not implement the optional higher-scope box. HJS/JAC, identity, authority and completeness claims require additional validators and evidence. Never normalize signed payloads with an unrelated JSON format.
