import time
import logging
from functools import wraps
from prometheus_client import Counter, Histogram, Summary

# Metrics
LLM_REQUEST_COUNT = Counter('llm_requests_total', 'Total LLM calls', ['model', 'agent'])
LLM_LATENCY = Histogram('llm_latency_seconds', 'LLM response latency', ['model'])
TOKEN_USAGE = Counter('llm_token_usage_total', 'Total tokens consumed', ['model', 'type'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmartSupport-Enterprise")

def trace_llm_call(model_name: str, agent_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            LLM_REQUEST_COUNT.labels(model=model_name, agent=agent_name).inc()
            
            try:
                result = func(*args, **kwargs)
                latency = time.time() - start_time
                LLM_LATENCY.labels(model=model_name).observe(latency)
                
                logger.info(f"LLM Call | Agent: {agent_name} | Model: {model_name} | Latency: {latency:.2f}s")
                return result
            except Exception as e:
                logger.error(f"LLM Error | Agent: {agent_name} | Model: {model_name} | Error: {str(e)}")
                raise e
        return wrapper
    return decorator

def log_token_usage(model: str, prompt_tokens: int, completion_tokens: int):
    TOKEN_USAGE.labels(model=model, type='prompt').inc(prompt_tokens)
    TOKEN_USAGE.labels(model=model, type='completion').inc(completion_tokens)
    logger.info(f"Tokens | Model: {model} | Total: {prompt_tokens + completion_tokens}")
