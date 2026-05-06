# Replay Verification Diagram

This diagram shows the verification path before a replay result is accepted as trustworthy.

```mermaid
flowchart LR
    Archive["Archive\nJAC records\nraw evidence pointers"]
    Canonicalization["Canonicalization\nstable ordering\nnormalized encodings"]
    HashVerification["Hash Verification\nrecord digests\nsignature checks"]
    LineageVerification["Lineage Verification\ndelegation chain\npolicy continuity"]
    Result{"Result\nverified?"}
    Accepted["Accept Replay\nshow deterministic trace"]
    Rejected["Reject Replay\nreport mismatch + record id"]

    Archive --> Canonicalization
    Canonicalization --> HashVerification
    HashVerification --> LineageVerification
    LineageVerification --> Result
    Result -->|yes| Accepted
    Result -->|no| Rejected

    classDef archive fill:#fff7e6,stroke:#d99000,stroke-width:1.5px,color:#172033;
    classDef verify fill:#e8f1ff,stroke:#2f6fed,stroke-width:1.5px,color:#172033;
    classDef pass fill:#edf8f0,stroke:#2c8a4a,stroke-width:1.5px,color:#172033;
    classDef fail fill:#fff0f0,stroke:#d64545,stroke-width:1.5px,color:#172033;
    class Archive archive;
    class Canonicalization,HashVerification,LineageVerification,Result verify;
    class Accepted pass;
    class Rejected fail;
```

## Developer notes

- Canonicalization must happen before hashing; otherwise equivalent records can produce different digests.
- Hash verification answers whether stored content changed.
- Lineage verification answers whether the delegation chain and policy claims still make sense together.
- Rejected replays should produce actionable diagnostics: failed stage, expected digest, actual digest, and affected record id.
