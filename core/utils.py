from typing import List

def enhance_task_context(title: str, description: str, current_tags: List[str]) -> tuple[str, List[str]]:
    """
    Analyzes task content to infer priority and suggest tags.
    Returns (priority, tags).
    """
    priority = "medium"
    new_tags = set(current_tags)
    
    text = (title + " " + (description or "")).lower()
    
    # Priority Logic
    if any(word in text for word in ["urgent", "asap", "deadline", "important", "critical"]):
        priority = "high"
    elif any(word in text for word in ["low", "whenever", "maybe", "eventually"]):
        priority = "low"
    
    # Tag Logic
    if any(word in text for word in ["buy", "purchase", "shopping", "grocery"]):
        new_tags.add("shopping")
    if any(word in text for word in ["code", "debug", "api", "database", "deploy"]):
        new_tags.add("work")
    if any(word in text for word in ["gym", "run", "workout", "health"]):
        new_tags.add("health")
    if any(word in text for word in ["call", "email", "meet", "meeting"]):
        new_tags.add("communication")
        
    return priority, list(new_tags)
