import os
import time
from redis import Redis
from rq import Queue
from smartsupport_ai.ingestion.embed_store import ingest_to_chroma
from smartsupport_ai.core.observability import logger

redis_conn = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379))
)
q = Queue('smartsupport-tasks', connection=redis_conn)

def process_document_ingestion(file_path: str):
    logger.info(f"Worker | Starting ingestion for: {file_path}")
    # Simulating heavy processing
    time.sleep(5) 
    ingest_to_chroma()
    logger.info(f"Worker | Ingestion complete for: {file_path}")
    return True

def trigger_ingestion_task(file_path: str):
    job = q.enqueue(process_document_ingestion, file_path)
    return job.id
