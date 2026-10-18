from client import EnterpriseChatKnowledgeBaseAutoCurator

def main():
    curator = EnterpriseChatKnowledgeBaseAutoCurator()
    chat = [
        {"author": "Charlie", "text": "Redis cluster OOM kill on shard 2 after morning cron."},
        {"author": "David", "text": "Root cause was bigkey in analytics:user:sessions without TTL. Flushed key and added 24h expiration policy."},
        {"author": "Charlie", "text": "Verified working now, thanks!"}
    ]
    sop = curator.curate_knowledge_sop(chat, "Redis Shard OOM BigKey Remediation")
    print("--- Enterprise Auto-Curated SOP ---")
    print(sop['sop_markdown'])

if __name__ == "__main__":
    main()
