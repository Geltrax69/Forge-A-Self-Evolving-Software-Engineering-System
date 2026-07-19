"""Forge configuration. The model is interchangeable — change LLM_MODEL/LLM_BASE_URL
to point at LM Studio (http://localhost:1234/v1), Ollama, or anything OpenAI-compatible."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
PROMPTS = ROOT / "models" / "prompts"

# OpenAI-compatible endpoint. LM Studio default: http://localhost:1234/v1
LLM_BASE_URL = os.environ.get("FORGE_LLM_URL", "http://127.0.0.1:1234/v1")
LLM_MODEL = os.environ.get("FORGE_LLM_MODEL", "minicpm5-1b")
LLM_API_KEY = os.environ.get("FORGE_LLM_KEY", "not-needed")  # local servers ignore it
EMBED_MODEL = os.environ.get("FORGE_EMBED_MODEL", "text-embedding-nomic-embed-text-v1.5")

# 1B only. Every stage runs on minicpm5-1b — the whole point is that the
# evidence + verify + auto-repair pipeline makes a tiny model reliable, not a big one.
STAGE_MODELS = {
    "intent":  os.environ.get("FORGE_INTENT_MODEL", LLM_MODEL),
    "planner": os.environ.get("FORGE_PLANNER_MODEL", LLM_MODEL),
    "coder":   os.environ.get("FORGE_CODER_MODEL", LLM_MODEL),
}

# Knowledge router: keyword -> doc folders to load. First real routing "brain".
# ponytail: plain substring map. Upgrade to embeddings only if keyword routing misses.
ROUTES = {
    "go":         ["backend/Go"],
    "golang":     ["backend/Go"],
    "chi":        ["backend/Chi"],
    "router":     ["backend/Chi"],
    "sqlc":       ["backend/SQLC"],
    "query":      ["backend/SQLC"],
    "postgres":   ["database/PostgreSQL"],
    "postgresql": ["database/PostgreSQL"],
    "database":   ["database/PostgreSQL"],
    "sql":        ["database/PostgreSQL", "backend/SQLC"],
    "redis":      ["cache/Redis"],
    "cache":      ["cache/Redis"],
    "jwt":        ["auth/JWT"],
    "token":      ["auth/JWT"],
    "oauth":      ["auth/OAuth"],
    "auth":       ["auth/JWT", "auth/OAuth"],
    "login":      ["auth/JWT", "backend/Chi"],
    "authentication": ["auth/JWT", "auth/OAuth"],
    "docker":     ["deployment/Docker"],
    "container":  ["deployment/Docker"],
    "nginx":      ["deployment/Nginx"],
    "proxy":      ["deployment/Nginx"],
    "s3":         ["objectstorage/S3"],
    "storage":    ["objectstorage/S3"],
    "upload":     ["objectstorage/S3"],
    "next":       ["frontend/NextJS"],
    "nextjs":     ["frontend/NextJS"],
    "react":      ["frontend/React"],
    "tailwind":   ["frontend/TailwindCSS"],
    "css":        ["frontend/TailwindCSS"],
    "ui":         ["frontend/Design/impeccable"],
    "design":     ["frontend/Design/impeccable"],
    "typescript": ["frontend/TypeScript"],
    "frontend":   ["frontend/NextJS", "frontend/React"],
}
