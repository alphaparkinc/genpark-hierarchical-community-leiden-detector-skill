"""
Example usage of Hierarchical Community Leiden Detector Skill.
"""

from client import CommunityDetector


def main():
    print("=== Hierarchical Community Detector Demonstration ===")
    detector = CommunityDetector(resolution=1.0)

    # Multi-domain agent memory graph with 2 distinct clusters:
    # Cluster A: Machine Learning / AI
    # Cluster B: Finance / Trading
    # Weak bridge between AI and Finance (Algorithmic Trading)
    edges = [
        ("PyTorch", "TensorFlow", 3.0),
        ("PyTorch", "Transformers", 4.0),
        ("Transformers", "LLM", 5.0),
        ("LLM", "RAG", 4.0),
        ("RAG", "VectorDB", 3.5),
        ("Stock_Market", "Portfolio", 4.0),
        ("Portfolio", "Risk_Model", 3.0),
        ("Risk_Model", "Bonds", 2.5),
        ("Stock_Market", "Options", 3.0),
        ("LLM", "Stock_Market", 0.5)  # Weak bridge edge
    ]

    res = detector.detect_communities(edges)
    print(f"Detected {res['community_count']} Communities across {res['total_nodes']} Nodes:")
    for idx, comm in enumerate(res["communities"]):
        print(f"\nCommunity {idx + 1} (Size: {len(comm)}):")
        print(" ", comm)


if __name__ == "__main__":
    main()
