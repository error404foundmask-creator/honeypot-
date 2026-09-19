from datetime import datetime, timezone
from sqlalchemy import create_engine, String, Integer, DateTime, Boolean, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
import os
url=os.getenv('DATABASE_URL','sqlite:///./honeypot.db')
engine=create_engine(url, connect_args={'check_same_thread':False} if url.startswith('sqlite') else {})
SessionLocal=sessionmaker(bind=engine, autocommit=False, autoflush=False)
class Base(DeclarativeBase): pass
class Event(Base):
    __tablename__='events'; id:Mapped[int]=mapped_column(primary_key=True); event_id:Mapped[str]=mapped_column(String(80),unique=True,index=True); timestamp:Mapped[datetime]=mapped_column(DateTime,index=True); source_ip:Mapped[str]=mapped_column(String(64),index=True); source_port:Mapped[int]=mapped_column(Integer); destination_port:Mapped[int]=mapped_column(Integer); protocol:Mapped[str]=mapped_column(String(20)); service:Mapped[str]=mapped_column(String(40),index=True); event_type:Mapped[str]=mapped_column(String(60),index=True); demo:Mapped[bool]=mapped_column(Boolean,default=False); risk_score:Mapped[int]=mapped_column(Integer,default=0,index=True); severity:Mapped[str]=mapped_column(String(10),index=True); threat_category:Mapped[str|None]=mapped_column(String(80),nullable=True)
class Alert(Base):
    __tablename__='alerts'; id:Mapped[int]=mapped_column(primary_key=True); event_id:Mapped[str]=mapped_column(String(80),index=True); severity:Mapped[str]=mapped_column(String(10)); message:Mapped[str]=mapped_column(Text); status:Mapped[str]=mapped_column(String(20),default='open'); created_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
class Service(Base):
    __tablename__='services'; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(40),unique=True); protocol:Mapped[str]=mapped_column(String(20)); port:Mapped[int]=mapped_column(Integer); status:Mapped[str]=mapped_column(String(20),default='online')
