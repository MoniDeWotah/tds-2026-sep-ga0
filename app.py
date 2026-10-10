import csv
import json
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentiment import classify

ROOT = Path(__file__).resolve().parent
TELEMETRY = json.loads((ROOT / 'telemetry.json').read_text())
with (ROOT / 'students.csv').open(newline='', encoding='utf-8') as file:
    STUDENTS = [{'studentId':int(row['studentId']), 'class':row['class']} for row in csv.DictReader(file)]
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['GET','POST','OPTIONS'], allow_headers=['*'])

class AnalyticsRequest(BaseModel):
    regions: list[str]
    threshold_ms: float = 180

def percentile(values, probability):
    values = sorted(values)
    position = (len(values)-1) * probability
    lower = int(position)
    upper = min(lower+1, len(values)-1)
    return values[lower] + (values[upper]-values[lower]) * (position-lower)

@app.post('/api/latency')
def latency(body: AnalyticsRequest):
    stats = []
    for region in body.regions:
        records = [r for r in TELEMETRY if r['region'] == region]
        if not records:
            continue
        latencies = [r['latency_ms'] for r in records]
        stats.append({
            'region':region,
            'avg_latency':round(sum(latencies)/len(records),2),
            'p95_latency':round(percentile(latencies,0.95),2),
            'avg_uptime':round(sum(r['uptime_pct'] for r in records)/len(records),3),
            'breaches':sum(r['latency_ms'] > body.threshold_ms for r in records)
        })
    return {'regions':stats}

@app.get('/api')
def students(classes: list[str] | None = Query(default=None, alias='class')):
    return {'students':STUDENTS if classes is None else [s for s in STUDENTS if s['class'] in classes]}

@app.get('/')
def home():
    return {'message':'TDS GA0 API', 'endpoints':['/api','/api/latency']}

class Sentences(BaseModel):
    sentences: list[str]

@app.post('/sentiment')
def sentiment(body: Sentences):
    return {'results':[{'sentence':text, 'sentiment':classify(text)} for text in body.sentences]}
