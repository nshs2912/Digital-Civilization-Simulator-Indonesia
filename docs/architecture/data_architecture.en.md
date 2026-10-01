# Data Architecture — v0.1

Primary data:
- Entities
- Relationships
- Claims
- Evidence
- Sources
- Temporal Context
- Spatial Context
- Provenance

**A Civilization Snapshot is not primary truth.** It is a derived/materialized view of the knowledge graph at a given time and place.

Flow:
Entity → Relationship → Claim → Evidence → Source → Provenance → Snapshot.

Evidence is immutable; claims and knowledge are versioned.