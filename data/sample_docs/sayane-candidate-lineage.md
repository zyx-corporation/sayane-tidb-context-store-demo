# Sayane Candidate and Lineage

Sayane treats captured context as a candidate before it becomes canonical context.

A captured insight should not be merged blindly. It should be evaluated, accepted or rejected, and recorded as lineage.

This workflow preserves the difference between temporary LLM output and reviewed user context.

For the TiDB Context Store demo, candidate and lineage concepts are represented as searchable context documents. Retrieval logs then show which candidate or lineage-related chunks were used during a query.

This sample demonstrates how Sayane-style audit trails can be tested in an enterprise Context Store backend.
