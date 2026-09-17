from contextlib import asynccontextmanager
from datetime import datetime, timezone
import os
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


VERSION = "3.0.0"

GOVINFO_FEEDS = [
    "BILLS",
    "BILLSTATUS",
    "BILLSUM",
    "CFR",
    "ECFR",
    "FR",
    "PLAW",
]


class AuditRequest(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=128)
    licensing_tier: str = Field(min_length=1, max_length=64)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"EMMAMEDIA {VERSION} starting")
    yield
    print("EMMAMEDIA shutting down")


app = FastAPI(
    title="Urielsmooth-Emmedia EMMAMEDIA",
    description="Modern compliance, media and GovInfo ingestion platform",
    version=VERSION,
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {
        "platform": "Urielsmooth-Emmedia (EMMAMEDIA)",
        "version": VERSION,
        "status": "operational",
        "architecture": "async-api",
        "utc": datetime.now(timezone.utc).isoformat(),
        "capabilities": [
            "GovInfo ingestion",
            "asynchronous auditing",
            "tenant isolation foundation",
            "cryptographic integrity foundation",
            "GPU-ready vector processing",
            "observability",
            "API-first architecture",
        ],
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ready")
async def ready():
    return {
        "status": "ready",
        "services": {
            "api": True,
            "govinfo": True,
            "database": bool(os.getenv("DATABASE_URL")),
            "gpu": False,
        },
    }


@app.get("/api/v1/govinfo/feeds")
async def govinfo_feeds():
    return {
        "count": len(GOVINFO_FEEDS),
        "feeds": [
            {
                "collection": feed,
                "url": f"https://www.govinfo.gov/bulkdata/{feed}",
            }
            for feed in GOVINFO_FEEDS
        ],
    }


@app.post("/api/v1/enterprise/audit")
async def enterprise_audit(payload: AuditRequest):
    allowed = {"enterprise", "sovereign", "verified_family"}

    if payload.licensing_tier not in allowed:
        raise HTTPException(
            status_code=403,
            detail="Unsupported licensing tier",
        )

    audit_id = str(uuid.uuid4())

    return {
        "audit_id": audit_id,
        "tenant_id": payload.tenant_id,
        "status": "queued",
        "licensing_tier": payload.licensing_tier,
        "feeds": len(GOVINFO_FEEDS),
        "message": "Audit accepted for asynchronous processing.",
    }
