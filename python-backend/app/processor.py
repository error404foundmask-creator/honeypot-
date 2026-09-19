from .database import Event
MOCK={'192.168.56.20': {'category':'lab_simulation','confidence':85,'reputation':'suspicious'}}
def lookup(ip):
    return MOCK.get(ip, {'category':'unknown','confidence':0,'reputation':'unavailable'})
def process(db, item):
    ti=lookup(item.source_ip); s=__import__('app.risk',fromlist=['score']).score(db,item); sev=__import__('app.risk',fromlist=['severity']).severity(s)
    e=Event(**item.model_dump(),risk_score=s,severity=sev,threat_category=ti['category']); db.add(e); db.commit(); db.refresh(e); return e,ti
