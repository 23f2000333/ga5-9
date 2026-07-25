from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator


# ------------------------
# Dossier
# ------------------------


class Line(BaseModel):
    lineId: str
    text: str


class Source(BaseModel):
    sourceId: str
    kind: str
    provenance: str
    title: str
    lines: List[Line]


class Dossier(BaseModel):
    dossierId: str
    partition: Literal["stable_core", "fresh_audit"]
    receivedAt: str
    mailbox: str
    objective: str
    sources: List[Source]


# ------------------------
# Receipt verifier
# ------------------------


class ReceiptVerifier(BaseModel):
    algorithm: Literal["Ed25519"]
    publicKeyJwk: Dict[str, Any]


# ------------------------
# propose request
# ------------------------


class Corpus(BaseModel):
    coreId: str
    auditId: str
    stableCount: int
    freshCount: int


class ProposeRequest(BaseModel):
    profile: Literal["ga5-mailroom-action-gate/v2"]

    operation: Literal["propose"]

    evaluationId: str

    receiptVerifier: ReceiptVerifier

    corpus: Corpus

    allowedActions: List[str]

    dossiers: List[Dossier]

    @model_validator(mode="after")
    def validate_unique_ids(self):

        ids = [x.dossierId for x in self.dossiers]

        if len(ids) != len(set(ids)):
            raise ValueError("duplicate dossier ids")

        return self


# ------------------------
# Proposal
# ------------------------


class Target(BaseModel):
    kind: str
    id: str


class Proposal(BaseModel):

    dossierId: str

    callId: str

    action: str

    target: Optional[Target] = None

    payload: Dict[str, Any] = Field(default_factory=dict)

    evidence: List[str]


class ProposeResponse(BaseModel):

    profile: Literal["ga5-mailroom-action-gate/v2"]

    evaluationId: str

    status: Literal["awaiting_receipts"]

    inputDigest: str

    proposals: List[Proposal]


# ------------------------
# Commit
# ------------------------


class Receipt(BaseModel):

    dossierId: str

    callId: str

    action: str

    accepted: bool

    proposalDigest: str

    receiptId: str

    receiptSignature: str


class CommitRequest(BaseModel):

    profile: Literal["ga5-mailroom-action-gate/v2"]

    operation: Literal["commit"]

    evaluationId: str

    inputDigest: str

    receipts: List[Receipt]

    @model_validator(mode="after")
    def unique_receipts(self):

        ids = [x.receiptId for x in self.receipts]

        if len(ids) != len(set(ids)):
            raise ValueError("duplicate receipt ids")

        return self


# ------------------------
# commit response
# ------------------------


class Outcome(BaseModel):

    dossierId: str

    callId: str

    action: str

    proposalDigest: str

    receiptId: str

    status: Literal["executed", "rejected"]


class CommitResponse(BaseModel):

    profile: Literal["ga5-mailroom-action-gate/v2"]

    evaluationId: str

    status: Literal["completed"]

    inputDigest: str

    outcomes: List[Outcome]
