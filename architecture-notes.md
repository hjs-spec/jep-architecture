# Architecture Notes

These notes describe how to use the diagrams when implementing the JEP / HJS / JAC runtime stack. They are intentionally practical and avoid product or whitepaper language.

## Layer responsibilities

### JEP: action envelope

JEP is the developer-facing contract for accountable work. It should answer:

- Who requested the action?
- Which agent or sub-agent is acting?
- What intent and constraints were delegated?
- Which tool or runtime operation is being requested?
- Which archive record should replay or verification use later?

JEP should not know how a specific SDK stores configuration or how a specific integration calls an external API.

### HJS: hardened job state

HJS carries execution state that needs integrity guarantees while work is in flight. It should include:

- signed or otherwise integrity-protected state claims;
- policy decisions that were evaluated before execution;
- execution constraints such as budget, time, tool scope, and retention rules;
- references to the parent delegation record when the action was delegated.

HJS should be validated before tool execution and archived after execution.

### JAC: accountability canon

JAC defines the canonical representation used by archive and replay code. It should include:

- stable field ordering and encoding rules;
- digest and signature fields;
- lineage identifiers;
- links to input, output, policy, and external evidence;
- replay verification outcomes.

JAC is the format developers should use when comparing records across runtimes or SDKs.

## Runtime implementation guidance

- Treat JEP middleware as the required entry point for accountable runtime actions.
- Keep the runtime dispatcher small: validate envelope, check HJS, call tool, capture result, write archive.
- Store both successful and failed tool executions.
- Record policy decisions alongside the action they authorized.
- Avoid storing raw secrets in archives; store redacted values, references, or sealed evidence blobs.
- Make replay read-only by default. Re-execution should be a separate explicit mode.

## Lineage fields developers should expect

A minimal lineage record should include:

| Field | Why it matters |
| --- | --- |
| `record_id` | Stable local id for the archived action. |
| `parent_record_id` | Connects agent, sub-agent, and tool delegations. |
| `actor_id` | Names the human, agent, sub-agent, or service that acted. |
| `delegated_by` | Names the upstream actor that granted authority. |
| `intent` | Explains why the action was taken. |
| `constraints` | Captures budget, scope, policy, and time limits. |
| `tool_id` | Identifies the tool or capability invoked. |
| `input_digest` | Detects input changes without requiring every consumer to load raw input. |
| `output_digest` | Detects output changes and supports replay comparison. |
| `external_reference` | Correlates the record with an outside system when one exists. |

## Verification flow

Replay verification should run in this order:

1. Load the archive record and required evidence.
2. Canonicalize the record using JAC rules.
3. Verify hashes and signatures.
4. Verify lineage from the current record back to the root human or organization authority.
5. Return a verified trace or a structured failure.

This order matters because lineage verification is only meaningful after the record content has passed canonical hash checks.

## Development checklist

Use this checklist when adding a new runtime feature, SDK method, or integration:

- Does the action enter through JEP middleware?
- Is HJS validated before any external side effect?
- Is every delegation hop represented in lineage metadata?
- Are inputs, outputs, policy decisions, and external ids archived?
- Can replay verify the record without calling the live external system?
- Are trust boundaries explicit in code, configuration, and logs?
- Can failures be archived and diagnosed with record ids?
