# incentive-engine-api/api/db/models.py

from sqlalchemy import (
    Column, Integer, String, DateTime, Float, ForeignKey, JSON
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class DeveloperAccount(Base):
    """
    Maps each API user (by api_key) to its own custodial sub-wallet.
    """
    __tablename__ = "developer_accounts"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, unique=True, nullable=False, index=True)
    wallet_id = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Backref from rewards
    rewards = relationship("Reward", back_populates="developer_account")


class Event(Base):
    """
    Records each incoming reward request before payout.
    """
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    developer_account_id = Column(
        Integer, ForeignKey("developer_accounts.id"), nullable=False
    )
    event_name = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    metadata = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    developer_account = relationship("DeveloperAccount")
    rewards = relationship("Reward", back_populates="event")


class Reward(Base):
    """
    Tracks individual reward transactions tied to an Event.
    """
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    developer_account_id = Column(
        Integer, ForeignKey("developer_accounts.id"), nullable=False
    )
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # e.g., pending, paid, failed
    tx_hash = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    event = relationship("Event", back_populates="rewards")
    developer_account = relationship("DeveloperAccount", back_populates="rewards")


class UserBalance(Base):
    """
    Caches the current USDC balance for each user per developer.
    """
    __tablename__ = "user_balances"

    id = Column(Integer, primary_key=True, index=True)
    developer_account_id = Column(
        Integer, ForeignKey("developer_accounts.id"), nullable=False
    )
    user_id = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    developer_account = relationship("DeveloperAccount")
