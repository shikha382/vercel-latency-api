from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import statistics

app = FastAPI()

# Enable CORS (required)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestBody(BaseModel):
    regions: List[str]
    threshold_ms: int

@app.post("/api/latency")
def latency_metrics(data: RequestBody):
    results: Dict[str, Dict] = {}

    for region in data.regions:
        # dummy latency values (example)
        latencies = [100, 120, 130, 150, 170]

        avg_latency = statistics.mean(latencies)
        p95_latency = sorted(latencies)[int(0.95 * len(latencies)) - 1]
        avg_uptime = 99.9
        breaches = sum(1 for l in latencies if l > data.threshold_ms)

        results[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches,
        }

    return results
