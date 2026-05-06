# Trust Boundary Diagram

This diagram separates the principals and systems that participate in an accountable action.

```mermaid
flowchart TB
    subgraph HumanBoundary["Human trust boundary"]
        Human["Human\nintent owner\napproval source"]
    end

    subgraph AgentBoundary["Agent trust boundary"]
        Agent["Agent\nplanner\nstateful reasoning"]
    end

    subgraph OrgBoundary["Organization trust boundary"]
        Policy["Organization Policy\npermissions\nbudgets\nretention"]
        Archive["Accountability Archive\ncanonical records\naudit retention"]
    end

    subgraph ToolBoundary["Tool trust boundary"]
        Tool["Tool\ntyped capability\ninput/output contract"]
    end

    subgraph ExternalBoundary["External system trust boundary"]
        External["External System\nthird-party API\nfiles\nservices"]
    end

    Human -->|intent + approval| Agent
    Agent -->|policy check| Policy
    Policy -->|allowed scope| Agent
    Agent -->|JEP envelope + HJS| Tool
    Tool -->|side effect request| External
    External -->|response| Tool
    Tool -->|evidence| Archive
    Agent -->|decision trace| Archive
    Archive -->|audit / replay report| Human

    classDef human fill:#e8f1ff,stroke:#2f6fed,stroke-width:1.5px,color:#172033;
    classDef org fill:#fff7e6,stroke:#d99000,stroke-width:1.5px,color:#172033;
    classDef runtime fill:#edf8f0,stroke:#2c8a4a,stroke-width:1.5px,color:#172033;
    classDef external fill:#fff0f0,stroke:#d64545,stroke-width:1.5px,color:#172033;
    class Human human;
    class Agent,Tool runtime;
    class Policy,Archive org;
    class External external;
```

## Developer notes

- Do not assume agent memory, organization policy, tool code, and external systems share a trust boundary.
- Policy decisions should be recorded with the action they authorize.
- Tool outputs need validation before they become agent context.
- External system identifiers are useful for audit correlation, but they should not replace canonical archive ids.
