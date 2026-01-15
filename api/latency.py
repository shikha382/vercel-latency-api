from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import statistics

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
with open("q-vercel-latency.json", "r") as f:
    DATA = json.load(f)

@app.post("/api/latency")
async def latency(req: Request):
    body = await req.json()
    regions = body["regions"]
    threshold = body["threshold_ms"]

    filtered = [r for r in DATA if r["region"] in regions]

    latencies = [r["latency_ms"] for r in filtered]
    uptimes = [r["uptime_pct"] for r in filtered]

    avg_latency = sum(latencies) / len(latencies)
    p95_latency = sorted(latencies)[int(0.95 * len(latencies)) - 1]
    avg_uptime = sum(uptimes) / len(uptimes)
    breaches = sum(1 for l in latencies if l > threshold)

    return {
        "avg_latency": round(avg_latency, 2),
        "p95_latency": round(p95_latency, 2),
        "avg_uptime": round(avg_uptime, 2),
        "breaches": breaches
    }
