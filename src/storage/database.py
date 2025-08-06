# src/storage/database.py
"""Data persistence layer implementation."""
import logging
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.settings import Settings

Base = declarative_base()

class Transaction(Base):
    """Database model for transactions."""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    tx_id = Column(String)
    timestamp = Column(Float)
    amount = Column(Float)
    currency = Column(String)
    status = Column(String)

class Database:
    """
    Database management class.
    
    Handles data persistence and retrieval operations.
    """
    def __init__(self, config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.config = {**Settings().get_default_settings()['database'], **config}
        self.engine = self._initialize_engine()
        Base.metadata.create_all(self.engine)
        
    def _initialize_engine(self) -> Any:
        """Initialize database engine."""
        url = self.config['connection_url']
        return create_engine(url, pool_pre_ping=True)
        
    def record_transaction(self, tx_data: Dict[str, Any]) -> None:
        """Record transaction in database."""
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        try:
            transaction = Transaction(
                tx_id=tx_data['tx_id'],
                timestamp=datetime.utcnow().timestamp(),
                amount=tx_data['amount'],
                currency=tx_data['currency'],
                status='pending'
            )
            
            session.add(transaction)
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            session.close()
