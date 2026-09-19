from collections import defaultdict
from .database import Event

def score(db, incoming):
    prior=db.query(Event).filter(Event.source_ip==incoming.source_ip).all(); services={e.service for e in prior}; score=20 if not prior else 15
    score += 25 if incoming.service not in services and len(services)>=2 else 0
    score += 20 if len(prior)>=3 else 0
    score += 20 if incoming.event_type not in ('connection_attempt','demo_connection') else 0
    if incoming.source_ip.startswith('192.168.56.'): score += 10
    return min(score,100)
def severity(score): return 'CRITICAL' if score>=80 else 'HIGH' if score>=60 else 'MEDIUM' if score>=30 else 'LOW'
