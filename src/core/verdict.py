"""Core verdict data models for paper filtering."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class VerdictDecision(str, Enum):
    """Final decision labels for paper triage."""

    REJECT = "Reject"
    SKIM = "Skim"
    MUST_READ = "Must Read"


class PaperAnalysisResult(BaseModel):
    """Structured analysis result returned by LLM-based reviewer."""

    model_config = ConfigDict(extra="forbid")

    verdict: VerdictDecision = Field(
        description='Decision: "Reject" / "Skim" / "Must Read".'
    )
    score: int = Field(
        ge=0,
        le=10,
        description="Overall score. Normal range is 1-10; 0 is reserved for degraded fallback.",
    )
    novelty_delta: str = Field(
        min_length=1, description="Compared with baseline, where is the gain?"
    )
    mechanism_summary: str = Field(min_length=1, description="Core mechanism summary.")
    critical_flaws: list[str] = Field(
        default_factory=list, description="Critical flaws and attack points."
    )
