# src/storage/metrics_repository.py
"""Metrics storage and retrieval system."""
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy import create_engine, Column, Float, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.settings import Settings

Base = declarative_base()

class Metric(Base):
    """Database model for storing metrics."""
    __tablename__ = 'metrics'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True)
    agent_id = Column(String)
    metric_type = Column(String)
    value = Column(Float)
    metadata = Column(String)

class MetricsRepository:
    """Handles storage and retrieval of system metrics."""
    def __init__(self, config: Dict[str, Any]):
        self.config = {**Settings().get_default_settings()['metrics'], **config}
        self.engine = self._initialize_engine()
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def _initialize_engine(self) -> Any:
        """Initialize database engine with connection pooling."""
        url = self.config['connection_url']
        return create_engine(url, pool_size=20, max_overflow=10)
        
    def store_metric(self, metric_data: Dict[str, Any]) -> bool:
        """Store a metric in the database."""
        session = self.Session()
        try:
            metric = Metric(
                timestamp=datetime.utcnow(),
                agent_id=metric_data['agent_id'],
                metric_type=metric_data['type'],
                value=metric_data['value'],
                metadata=str(metric_data.get('metadata', {}))
            )
            
            session.add(metric)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def get_metrics(self, 
                    agent_id: Optional[str] = None,
                    metric_type: Optional[str] = None,
                    start_time: Optional[datetime] = None,
                    end_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Retrieve metrics with optional filtering."""
        session = self.Session()
        try:
            query = session.query(Metric)
            
            if agent_id:
                query = query.filter(Metric.agent_id == agent_id)
            if metric_type:
                query = query.filter(Metric.metric_type == metric_type)
            if start_time:
                query = query.filter(Metric.timestamp >= start_time)
            if end_time:
                query = query.filter(Metric.timestamp <= end_time)
                
            return [{
                'timestamp': m.timestamp,
                'agent_id': m.agent_id,
                'type': m.metric_type,
                'value': m.value,
                'metadata': eval(m.metadata) if m.metadata else {}
            } for m in query.all()]
        finally:
            session.close()
