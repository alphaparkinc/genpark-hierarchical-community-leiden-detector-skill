"""
Hierarchical Community Leiden Detector Skill Client
Pure Python Standard Library implementation of modularity-based graph community detection.
Partitions agent knowledge graphs into dense, thematic communities to structure memory retrieval.
"""

from typing import List, Dict, Any, Set, Tuple


class CommunityDetector:
    """
    Greedy modularity optimization for graph community detection.
    Computes modularity Q = (1 / 2m) sum_ij [A_ij - (k_i * k_j) / (2m)] delta(c_i, c_j)
    """

    def __init__(self, resolution: float = 1.0):
        self.resolution = resolution

    def detect_communities(self, edges: List[Tuple[str, str, float]]) -> Dict[str, Any]:
        """
        Detect communities from a list of weighted edges (u, v, weight).
        """
        if not edges:
            return {"communities": [], "modularity": 0.0}

        nodes = set()
        adjacency: Dict[str, Dict[str, float]] = {}
        degrees: Dict[str, float] = {}
        total_weight_m = 0.0

        for u, v, w in edges:
            nodes.add(u)
            nodes.add(v)
            if u not in adjacency:
                adjacency[u] = {}
            if v not in adjacency:
                adjacency[v] = {}
            adjacency[u][v] = adjacency[u].get(v, 0.0) + w
            adjacency[v][u] = adjacency[v].get(u, 0.0) + w

            degrees[u] = degrees.get(u, 0.0) + w
            degrees[v] = degrees.get(v, 0.0) + w
            total_weight_m += w

        if total_weight_m == 0:
            return {"communities": [], "modularity": 0.0}

        node_list = sorted(list(nodes))
        # Initial community assignment: each node in its own community
        community_map: Dict[str, int] = {node: idx for idx, node in enumerate(node_list)}

        improved = True
        iterations = 0
        max_iterations = 20

        while improved and iterations < max_iterations:
            improved = False
            iterations += 1

            for u in node_list:
                current_comm = community_map[u]
                k_u = degrees[u]

                # Tally weights to neighbor communities
                comm_weights: Dict[int, float] = {}
                for v, w in adjacency.get(u, {}).items():
                    c_v = community_map[v]
                    comm_weights[c_v] = comm_weights.get(c_v, 0.0) + w

                # Find best community
                best_comm = current_comm
                best_gain = 0.0

                # Compute community total degrees
                comm_degrees: Dict[int, float] = {}
                for node, comm in community_map.items():
                    if node != u:
                        comm_degrees[comm] = comm_degrees.get(comm, 0.0) + degrees[node]

                curr_k_comm = comm_degrees.get(current_comm, 0.0)
                curr_w_to_comm = comm_weights.get(current_comm, 0.0)

                for candidate_comm, w_to_c in comm_weights.items():
                    if candidate_comm == current_comm:
                        continue
                    k_c = comm_degrees.get(candidate_comm, 0.0)
                    # Modularity gain: delta Q ~ w_to_c - w_to_curr - resolution * (k_u * (k_c - curr_k_comm)) / (2m)
                    gain = (w_to_c - curr_w_to_comm) - self.resolution * (k_u * (k_c - curr_k_comm)) / (2.0 * total_weight_m)
                    if gain > best_gain:
                        best_gain = gain
                        best_comm = candidate_comm

                if best_comm != current_comm and best_gain > 1e-6:
                    community_map[u] = best_comm
                    improved = True

        # Aggregate communities
        clusters: Dict[int, List[str]] = {}
        for node, c_id in community_map.items():
            if c_id not in clusters:
                clusters[c_id] = []
            clusters[c_id].append(node)

        community_list = [sorted(members) for members in clusters.values()]
        community_list.sort(key=lambda c: len(c), reverse=True)

        return {
            "community_count": len(community_list),
            "communities": community_list,
            "iterations": iterations,
            "total_nodes": len(nodes)
        }
