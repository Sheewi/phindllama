# src/storage/transaction_logger.py
"""Transaction logging system with web integration."""
from datetime import datetime
from typing import Dict, Any, Optional
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.settings import Settings

Base = declarative_base()

class Transaction(Base):
    """Database model for transactions."""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    tx_id = Column(String)
    timestamp = Column(DateTime, index=True)
    agent_id = Column(String)
    type = Column(String)
    amount = Column(Float)
    currency = Column(String)
    status = Column(String)
    metadata = Column(String)

class TransactionLogger:
    """Handles transaction logging and web notifications."""
    def __init__(self, config: Dict[str, Any]):
        self.config = {**Settings().get_default_settings()['transactions'], **config}
        self.engine = self._initialize_engine()
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.logger = logging.getLogger(__name__)
        
    def _initialize_engine(self) -> Any:
        """Initialize database engine with connection pooling."""
        url = self.config['connection_url']
        return create_engine(url, pool_size=20, max_overflow=10)
        
    def log_transaction(self, tx_data: Dict[str, Any]) -> bool:
        """Log a transaction and send web notification."""
        session = self.Session()
        try:
            transaction = Transaction(
                tx_id=tx_data['tx_id'],
                timestamp=datetime.utcnow(),
                agent_id=tx_data['agent_id'],
                type=tx_data['type'],
                amount=tx_data['amount'],
                currency=tx_data['currency'],
                status=tx_data['status'],
                metadata=str(tx_data.get('metadata', {}))
            )
            
            session.add(transaction)
            session.commit()
            
            # Send web notification
            self._notify_web(tx_data)
            return True
        except Exception as e:
            session.rollback()
            self.logger.error(f"Transaction logging failed: {str(e)}")
            raise
        finally:
            session.close()
            
    def _notify_web(self, tx_data: Dict[str, Any]) -> None:
        """Send transaction notification to web interface."""
        try:
            import requests
            notification_url = self.config['web_notification_url']
            requests.post(
                notification_url,
                json={
                    'tx_id': tx_data['tx_id'],
                    'amount': tx_data['amount'],
                    'currency': tx_data['currency'],
                    'status': tx_data['status']
                }
            )
        except Exception as e:
            self.logger.error(f"Web notification failed: {str(e)}")
