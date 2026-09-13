# Architecture notes

These implementation notes explain the diagrams. Protocol definitions remain in [JEP-Core-0.6](https://github.com/hjs-spec/jep-v06), [HJS 0.5](https://github.com/hjs-spec/hjs-05) and [JAC](https://github.com/hjs-spec/jac-agent-02).

## Responsibilities

| Layer | Owns | Does not establish by itself |
|---|---|---|
| JEP: Judgment Event Protocol | Atomic signed J/D/T/V statements, Core canonicalization, signatures, event hashes and verification results | Truth, complete logging, identity binding or valid authority |
| HJS | Archive, privacy, receipt and evidence lifecycle | New JEP verbs, signature rules, Core levels or execution permissions |
| JAC | Declared dependencies over JEP/HJS, including `ext["https://jac.org/chain"]` with `based_on`, `based_on_type`, `relation` | Core canonicalization or proof of real causality |
| Application runtime | Tool dispatch, independently configured policy, identity resolution and storage integration | Automatic conformance to all three protocols |
| SDK/API | Supported event creation and verification interfaces | Authority validation merely because a signature passes |

## Core objects and application envelopes

Preserve signed Core members exactly when forwarding or archiving. The protocol profile is `jep-core-0.6`, while its wire member is `jep: "1"`. Software version numbers are independent.

Application fields such as `record_id`, `sequence`, `event_hash`, `previous_event_hash`, tool digests and external references belong to an explicitly defined local envelope or permitted extension. They are not a universal set of required Core members. Do not append them to an already signed Core object or replace its canonicalization with ordinary sorted JSON.

A Core `D` event is a declaration. Enforcing permissions before a tool side effect requires the application's policy and trust model. A `T` event does not undo an external side effect. A `V` statement must describe the checks actually performed, with its scope preserved; it does not elevate a Level 1 result to full authority verification.

## Verification and replay

1. Parse strictly and select an explicit format/profile. Historical formats require explicit compatibility paths.
2. Validate Core syntax, canonicalize according to Core rules and verify the signature under an independently trusted key policy.
3. Return the actual `profile`, `level`, `mode`, `scopes`, `conformance_class`, diagnostics and event hash.
4. If required and supported, separately validate archive receipts, declared dependencies, identity binding and application authority. Report missing evidence as unresolved or failed under that validator's contract.

The current reference API performs Level 1 syntax and cryptographic verification. It does not perform full HJS/JAC, identity or authority checks. Archival mode verifies existing evidence; live anti-replay consumption is an explicit different operation. A locally recomputed hash chain lacks a trusted completeness anchor and can be rewritten by its author.

## Runtime integration

Capture successful and failed operations according to the application's recording policy, minimize sensitive data, and preserve links to independently available evidence. Recording may fail after a tool side effect, so middleware alone does not guarantee complete or atomic logging. Replay should be read-only; re-executing tools is a separate explicit action. Keep policy decisions, signing-key trust, execution permissions and retention rules visible as distinct responsibilities.
