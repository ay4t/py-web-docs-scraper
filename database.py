from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create database engine
engine = create_engine('sqlite:///docs_scraper.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Documentation(Base):
    __tablename__ = 'documentations'
    
    id = Column(Integer, primary_key=True)
    base_url = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DocumentationLink(Base):
    __tablename__ = 'documentation_links'
    
    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    title = Column(String)
    is_processed = Column(Boolean, default=False)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
