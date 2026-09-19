import asyncio
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from .database import Base, engine, SessionLocal, Event, Alert, Service
from .schemas import EventIn, EventOut, AlertOut
from .processor import process
Base.metadata.create_all(engine)
app=FastAPI(title='Honeypot Analysis API', version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
clients=set()
def db():
    s=SessionLocal()
    try: yield s
    finally: s.close()
async def broadcast(data):
    dead=[]
    for ws in clients:
        try: await ws.send_json(data)
        except Exception: dead.append(ws)
    for ws in dead: clients.discard(ws)
@app.get('/api/health')
def health(): return {'status':'ok','services':4}
@app.post('/api/events',response_model=EventOut)
async def create(item:EventIn, session=Depends(db)):
    try: event,ti=process(session,item)
    except Exception as ex: raise HTTPException(400,str(ex))
    if event.severity in ('HIGH','CRITICAL'):
        alert=Alert(event_id=event.event_id,severity=event.severity,message=f'{event.severity}-risk activity from {event.source_ip} targeting {event.service}'); session.add(alert); session.commit()
    data=EventOut.model_validate(event).model_dump(mode='json'); data['threat_intelligence']=ti; await broadcast({'type':'event','event':data}); return event
@app.get('/api/events',response_model=list[EventOut])
def events(limit:int=50,session=Depends(db)): return session.query(Event).order_by(Event.timestamp.desc()).limit(min(limit,200)).all()
@app.get('/api/events/{event_id}',response_model=EventOut)
def event(event_id:str,session=Depends(db)):
    x=session.query(Event).filter(Event.event_id==event_id).first()
    if not x: raise HTTPException(404,'event not found')
    return x
@app.get('/api/alerts',response_model=list[AlertOut])
def alerts(session=Depends(db)): return session.query(Alert).order_by(Alert.created_at.desc()).limit(100).all()
@app.get('/api/statistics')
def stats(session=Depends(db)):
    return {'events':session.query(Event).count(),'high_risk':session.query(Event).filter(Event.severity.in_(['HIGH','CRITICAL'])).count(),'services':4,'active_alerts':session.query(Alert).filter(Alert.status=='open').count()}
@app.post('/api/demo/{service}',response_model=EventOut)
async def demo(service:str,session=Depends(db)):
    ports={'ssh':2222,'http':8080,'ftp':2121,'database':5433}; names={'ssh':'ssh_decoy','http':'http_decoy','ftp':'ftp_decoy','database':'db_decoy'}
    if service not in ports: raise HTTPException(400,'unknown demo service')
    from datetime import datetime,timezone
    import uuid
    item=EventIn(event_id=str(uuid.uuid4()),timestamp=datetime.now(timezone.utc),source_ip='192.168.56.20',source_port=49152,destination_port=ports[service],protocol=service.upper(),service=names[service],event_type='demo_connection',demo=True)
    return await create(item,session)
@app.websocket('/ws/events')
async def websocket(ws:WebSocket):
    await ws.accept(); clients.add(ws)
    try:
        while True: await ws.receive_text()
    except WebSocketDisconnect: clients.discard(ws)
