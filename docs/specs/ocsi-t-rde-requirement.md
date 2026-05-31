# OCSI T-RDE Requirement

## Status

Conceptual requirement draft.

This document defines how T-RDE should constrain implementations of OCSI: Open Context Store Interface.

## Purpose

OCSI implementations store and retrieve context that may later be used by LLMs, AI agents, RAG systems, or enterprise workflows.

Because retrieved context can change meaning when it is chunked, embedded, ranked, merged, summarized, or reused, OCSI implementations must preserve enough evidence for T-RDE-style evaluation.

The requirement is not that every retrieval must synchronously run a heavy evaluator.

The requirement is that every conforming OCSI implementation must preserve the structures needed for T-RDE review.

## Core requirement

An OCSI implementation must be T-RDE-compatible.

T-RDE compatibility means that the implementation can record, expose, and export enough evidence to evaluate meaning transformation across the context lifecycle.

At minimum, it must support traceability for:

```text
SourceRecord
  -> SearchUnit
      -> RetrievalEvent
          -> selected evidence
              -> AuditSummary
                  -> downstream generation or decision
```

## Why T-RDE is required

Without T-RDE compatibility, OCSI could degrade into a generic vector/search interface.

That would lose the core reason OCSI exists: context should remain inspectable, portable, and reviewable across tools and backends.

T-RDE is required because OCSI must distinguish:

- retrieval evidence from generated conclusions;
- permitted transformation from suspicious drift;
- source context from derived search units;
- backend scoring from semantic justification;
- lightweight audit summaries from full evaluation.

## Required evidence fields

A conforming OCSI implementation should preserve the following evidence fields where applicable.

### Source-level evidence

```text
source_id
source_uri
source_type
source_hash
created_at
updated_at
metadata
```

### Search-unit evidence

```text
unit_id
source_id
unit_index
content
content_hash
chunking_strategy
embedding_model
embedding_ref or embedding_hash
metadata
```

### Retrieval-event evidence

```text
retrieval_event_id
query
mode
backend_id
backend_capabilities
retrieved_unit_ids
scores
rank_order
selected_unit_ids
audit_summary
created_at
trace_metadata
```

### Transformation evidence

```text
preserved
transformed
inferred
unresolved
drift_risk
```

The exact schema may vary by backend, but the evidence must be recoverable.

## T-RDE checkpoints

OCSI implementations should expose checkpoints where T-RDE can be applied.

### 1. Ingestion checkpoint

Evaluates transformation from SourceRecord to SearchUnit.

Questions:

- Did chunking preserve the relevant context?
- Was any important source metadata lost?
- Does the SearchUnit overstate or narrow the source meaning?

### 2. Embedding checkpoint

Evaluates transformation from SearchUnit content to vector representation.

Questions:

- Which embedding model was used?
- Is the embedding version recorded?
- Can the embedding be regenerated or audited?
- Is semantic approximation being mistaken for ground truth?

### 3. Retrieval checkpoint

Evaluates transformation from query to retrieved evidence.

Questions:

- Which mode was used: lexical, vector, hybrid, or backend-native?
- Which units were retrieved and why?
- Were scores or ranks preserved?
- Was fallback behavior recorded?

### 4. Selection checkpoint

Evaluates transformation from retrieved units to selected evidence.

Questions:

- Which retrieved units were selected?
- Which retrieved units were excluded?
- Is there a reason or policy for selection?
- Is the merge policy inspectable?

### 5. Downstream-use checkpoint

Evaluates transformation from selected evidence to generated output, action, or decision.

Questions:

- Was the output grounded in selected evidence?
- Were inferred claims distinguished from preserved evidence?
- Were unresolved points kept visible?
- Did the output narrow, overstate, or distort the source context?

## Lightweight vs full T-RDE

OCSI should distinguish lightweight audit from full T-RDE evaluation.

### Lightweight audit

A minimal OCSI implementation may record:

```text
preserved
inferred
drift_risk
unresolved
```

This is useful for demos, logs, and small systems.

### Full T-RDE

A full T-RDE evaluator may use richer scoring, maps, policies, review outputs, or human evaluation.

OCSI does not define full T-RDE itself. It defines the evidence boundary that full T-RDE can consume.

## Conformance levels

### OCSI-Basic

Must support:

- SourceRecord storage;
- SearchUnit storage;
- RetrievalEvent logging;
- capability declaration;
- lightweight AuditSummary.

### OCSI-T-RDE-Ready

Must additionally support:

- source hash or equivalent provenance;
- chunking strategy record;
- embedding model/version record when embeddings are used;
- selected vs retrieved evidence separation;
- exportable trace bundle;
- explicit fallback recording.

### OCSI-T-RDE-Strict

Must additionally support:

- negative test cases for retrieval and audit behavior;
- stable evidence export format;
- backend capability snapshot per retrieval event;
- reviewable drift-risk classification;
- policy for promoting backend-specific features into the general interface.

## Requirement for OCSI implementations

A backend may implement OCSI only if it can satisfy at least OCSI-Basic.

A backend should not be recommended for enterprise or cross-agent use unless it can satisfy OCSI-T-RDE-Ready.

A backend should not be described as audit-grade unless it can satisfy OCSI-T-RDE-Strict or an equivalent reviewed profile.

## Relationship to Sayane

Sayane already treats captured context as reviewable candidates and records approved or rejected lineage.

OCSI should preserve that stance at the storage and retrieval layer.

For Sayane, T-RDE compatibility means:

- candidate context must not be silently merged into canonical context;
- lineage must remain inspectable;
- retrieval logs must preserve evidence used by later model output;
- lightweight audit must not be misrepresented as full T-RDE scoring;
- backend-specific retrieval behavior must not weaken Sayane's review-before-merge principle.

## Relationship to Sayane-TiDB demo

The current Sayane-TiDB demo satisfies parts of OCSI-Basic:

- documents are stored;
- chunks are stored;
- optional embeddings are stored;
- retrieval logs are stored;
- lightweight audit summaries are stored;
- text, vector, and hybrid modes are visible.

It does not yet satisfy OCSI-T-RDE-Ready because:

- chunking strategy is not fully recorded;
- embedding model/version is not stored per SearchUnit;
- fallback behavior is not fully recorded in RetrievalEvent;
- evidence export is not yet formalized;
- TiDB-native vector search is not implemented.

## RDE / Delta-M

- Preserved: OCSI remains backend-agnostic and evidence-centered.
- Transformed: OCSI implementation is now constrained by T-RDE compatibility.
- Added: conformance levels, checkpoints, and required evidence fields.
- Unresolved: exact formal schema for exportable trace bundles.
- Drift risk: T-RDE may be treated as a decorative label unless conformance tests are added.

## Next steps

1. Add this document as a normative constraint for future OCSI implementation work.
2. Update `open-context-store-interface.md` to reference this requirement.
3. Add a compliance checklist.
4. Add tests for evidence preservation in the Sayane-TiDB demo.
5. Promote the requirement to the main Sayane repository if OCSI is adopted there.
