#!/usr/bin/env python3
import json
import sys
from client import EnterpriseChatKnowledgeBaseAutoCurator

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        curator = EnterpriseChatKnowledgeBaseAutoCurator()
        msgs = [
            {"author": "Alice", "text": "PostgreSQL connection pool maxing out on pod-3", "is_solution_reaction": False},
            {"author": "Bob", "text": "Checking PgBouncer configuration now", "is_solution_reaction": False},
            {"author": "Bob", "text": "Fixed! Restarted PgBouncer and increased max_client_conn to 5000, latency dropped back to 4ms.", "is_solution_reaction": True}
        ]
        res = curator.curate_knowledge_sop(msgs, "PgBouncer Connection Saturation")
        assert res["solution_found"] is True
        assert res["verdict"] == "KNOWLEDGE_ARTICLE_GENERATED"
        print(f"[TEST PASS] Knowledge SOP Curated: {res['topic']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-knowledge-curator", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "curate_knowledge_sop", "description": "Curate chat discussion into formal knowledge SOP"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                curator = EnterpriseChatKnowledgeBaseAutoCurator()
                out = curator.curate_knowledge_sop(args.get("thread_messages", []), args.get("topic_context"))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
