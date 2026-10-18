"""
Enterprise Slack & WeCom Thread Knowledge Base Auto-Curator (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import re
from typing import Dict, Any, List, Optional

class EnterpriseChatKnowledgeBaseAutoCurator:
    SOLUTION_CUES = {"resolved", "fixed", "worked", "solution", "root cause", "verified", "thanks"}

    def __init__(self, curator_name: str = "GenPark-Knowledge-Distiller"):
        self.curator_name = curator_name

    def curate_knowledge_sop(self, thread_messages: List[Dict[str, Any]], topic_context: Optional[str] = None) -> Dict[str, Any]:
        if not thread_messages:
            return {"status": "EMPTY_THREAD", "sop_markdown": ""}
            
        initial_issue = thread_messages[0].get("text", "Unknown operational issue")
        initial_author = thread_messages[0].get("author", "Engineer")
        
        solution_candidates = []
        for msg in thread_messages[1:]:
            txt = msg.get("text", "").lower()
            if msg.get("is_solution_reaction") or any(cue in txt for cue in self.SOLUTION_CUES):
                solution_candidates.append(msg)
                
        best_solution = solution_candidates[-1].get("text", "Solution details discussed in thread.") if solution_candidates else "Solution pending confirmation."
        best_author = solution_candidates[-1].get("author", "SRE Lead") if solution_candidates else "Team"
        
        topic = topic_context or "Production Engineering Incident Resolution"
        
        sop_md = (
            f"# SOP Runbook: {topic}\n\n"
            f"**Reported Issue**: {initial_issue}\n"
            f"**Discovered By**: {initial_author}\n\n"
            f"## Verified Solution\n"
            f"{best_solution}\n\n"
            f"**Verified By**: {best_author}\n"
            f"**Status**: Curated & Auto-Cataloged into Knowledge Base"
        )
        
        return {
            "curator": self.curator_name,
            "topic": topic,
            "total_messages_condensed": len(thread_messages),
            "solution_found": len(solution_candidates) > 0,
            "sop_markdown": sop_md,
            "verdict": "KNOWLEDGE_ARTICLE_GENERATED"
        }
