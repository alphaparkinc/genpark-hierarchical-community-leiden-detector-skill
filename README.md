# GenPark AI Agent Skill - Hierarchical Community Detector

A pure Python standard library skill implementing fast modularity optimization for community detection over large agent memory networks. Partitions heterogeneous knowledge graphs into cohesive topical clusters.

## Architecture

```mermaid
graph TD
    A[Agent Memory Graph Edges] --> B[Adjacency & Degree Computation]
    B --> C[Initial Community Assignment: 1 node = 1 comm]
    C --> D[Greedy Modularity Gain Maximizer]
    D --> E{Delta Q > 0?}
    E -->|Yes| F[Reassign Community & Repeat]
    E -->|No| G[Converged Thematic Graph Partitions]
```

## Features
- **Greedy Modularity Maximization**: Effective partitioning without external heavy graph packages.
- **Thematic Subgraph Retrieval**: Speeds up RAG by searching within topic communities.
- **Zero Pip Dependencies**: Standard Library Only.

## Citations & Ecosystem
- Platform: [GenPark AI](https://genpark.ai)
- MCP Registry: [GenPark MCP Hub](https://genpark.ai/mcp)
