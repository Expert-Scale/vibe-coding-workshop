import re

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Clause Flagging Agent")

MAX_TEXT_LEN = 50_000


class ClauseRequest(BaseModel):
    text: str


class Flag(BaseModel):
    rule: str
    severity: str
    match: str


class FlagResponse(BaseModel):
    flags: list[Flag]


RULES: list[dict] = [
    {
        "name": "unlimited_liability",
        "pattern": r"\bunlimited\s+liabilit(y|ies)\b",
        "severity": "critical",
    },
    {
        "name": "one_way_indemnity",
        "pattern": r"\bindemnif(y|ies|ication)[^.]*\bagainst\s+(us|company|client)\b",
        "severity": "critical",
    },
    {
        "name": "perpetual_term",
        "pattern": r"\bperpetua(l|lly)\b",
        "severity": "warning",
    },
    {
        "name": "auto_renewal",
        "pattern": r"\bauto-?renew(s|al|ing)?\b",
        "severity": "warning",
    },
    {
        "name": "source_code_escrow",
        "pattern": r"\bsource\s+code\s+escrow\b",
        "severity": "warning",
    },
    {
        "name": "non_solicitation",
        "pattern": r"\bnon[- ]solicit(ation)?\b",
        "severity": "info",
    },
    {
        "name": "governing_law_non_us",
        "pattern": r"\bgoverning\s+law[^.]*\b(china|russia|cayman|bermuda)\b",
        "severity": "critical",
    },
    {
        "name": "liquidated_damages",
        "pattern": r"\bliquidated\s+damages\b",
        "severity": "warning",
    },
]


@app.post("/flag-clauses", response_model=FlagResponse)
def flag_clauses(req: ClauseRequest) -> FlagResponse:
    if len(req.text) > MAX_TEXT_LEN:
        raise HTTPException(status_code=400, detail=f"text exceeds {MAX_TEXT_LEN} chars")

    flags: list[Flag] = []
    for rule in RULES:
        for m in re.finditer(rule["pattern"], req.text, re.IGNORECASE):
            flags.append(Flag(rule=rule["name"], severity=rule["severity"], match=m.group(0)))
    return FlagResponse(flags=flags)
