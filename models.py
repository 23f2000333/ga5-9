from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Text

from database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    evaluation_id = Column(String, primary_key=True)
    input_digest = Column(String)
    request_hash = Column(String)
    public_key = Column(Text)


class ProposalCache(Base):
    __tablename__ = "proposal_cache"

    fingerprint = Column(String, primary_key=True)
    proposal_json = Column(Text)
    call_id = Column(String)


class Proposal(Base):
    __tablename__ = "proposals"

    proposal_digest = Column(String, primary_key=True)

    evaluation_id = Column(String)
    dossier_id = Column(String)

    call_id = Column(String)

    proposal_json = Column(Text)


class Receipt(Base):
    __tablename__ = "receipts"

    receipt_id = Column(String, primary_key=True)

    evaluation_id = Column(String)

    dossier_id = Column(String)

    call_id = Column(String)

    accepted = Column(Boolean)

    verified = Column(Boolean)

    signature = Column(Text)
