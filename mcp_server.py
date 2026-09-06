"""
MCP Server for Hierarchical Community Leiden Detector Skill.
"""

import json
import sys
from client import CommunityDetector

DETECTOR = CommunityDetector()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "detect_communities",
                    "description": "Partition graph edges into modular communities",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "edges": {
                                "type": "array",
                                "items": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "resolution": {"type": "number", "default": 1.0}
                        },
                        "required": ["edges"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "detect_communities":
            edges_raw = args["edges"]
            edges = []
            for e in edges_raw:
                u, v = e[0], e[1]
                w = float(e[2]) if len(e) > 2 else 1.0
                edges.append((u, v, w))

            DETECTOR.resolution = args.get("resolution", 1.0)
            res = DETECTOR.detect_communities(edges)
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
