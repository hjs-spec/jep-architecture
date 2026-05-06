# Protocol Stack Diagram

This diagram shows the layer order developers should preserve when adding runtime features or integrations.

```mermaid
flowchart TB
    JEP["JEP\nJob Envelope Protocol\n- action envelope\n- actor and delegation metadata\n- replay references"]
    HJS["HJS\nHardened Job State\n- signed job state\n- policy claims\n- execution constraints"]
    JAC["JAC\nJob Accountability Canon\n- canonical records\n- archive schema\n- verification contract"]
    Runtime["Runtime\n- agent loop\n- middleware hooks\n- tool dispatcher"]
    SDKs["SDKs\n- typed builders\n- validators\n- replay clients"]
    Integrations["Integrations\n- tools\n- external APIs\n- workflow systems"]

    JEP -->|wraps and names accountable work| HJS
    HJS -->|pins mutable execution state| JAC
    JAC -->|defines archive and replay rules for| Runtime
    Runtime -->|exposes stable APIs through| SDKs
    SDKs -->|connect applications to| Integrations

    classDef protocol fill:#e8f1ff,stroke:#2f6fed,stroke-width:1.5px,color:#172033;
    classDef execution fill:#edf8f0,stroke:#2c8a4a,stroke-width:1.5px,color:#172033;
    classDef edge fill:#fff7e6,stroke:#d99000,stroke-width:1.5px,color:#172033;
    class JEP,HJS,JAC protocol;
    class Runtime execution;
    class SDKs,Integrations edge;
```

## Developer notes

- Keep protocol data models (`JEP`, `HJS`, `JAC`) independent from runtime implementation details.
- Runtime code should depend on protocol contracts, not on a specific SDK or integration.
- SDKs should make valid envelopes easy to build and invalid state hard to submit.
- Integrations should be replaceable as long as they preserve tool input, output, and lineage records.
