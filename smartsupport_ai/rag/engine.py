import os
import asyncio
from typing import List, Dict, Any
from functools import lru_cache
import google.generativeai as genai
from smartsupport_ai.db.models import Customer, Order, Ticket
from smartsupport_ai.db.database import SessionLocal
from smartsupport_ai.ingestion.embed_store import VectorStore
from smartsupport_ai.core.observability import trace_llm_call, logger

class OptimizedRAGEngine:
    _instance = None

    def __new__(cls):
        """Singleton Pattern to prevent multiple DB/Vector connections"""
        if cls._instance is None:
            cls._instance = super(OptimizedRAGEngine, cls).__new__(cls)
            cls._instance._init_engine()
        return cls._instance

    def _init_engine(self):
        self.vector_store = VectorStore()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-flash-latest')

    @lru_cache(maxsize=100)
    def _cached_knowledge_search(self, query: str) -> str:
        """LRU Cache for expensive vector searches"""
        return self.vector_store.search(query)

    async def get_customer_context_async(self, customer_id: str) -> str:
        """Asynchronous retrieval of customer history"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_get_context, customer_id)

    def _sync_get_context(self, customer_id: str) -> str:
        with SessionLocal() as db:
            customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
            if not customer: return "Unknown Customer"
            
            # Efficient query with selective columns (optimization)
            orders = db.query(Order.order_id, Order.shipping_status).filter(Order.customer_id == customer_id).limit(3).all()
            
            context = f"Member: {customer.name} | Plan: {customer.membership_plan}\nOrders: "
            context += ", ".join([f"{o.order_id}({o.shipping_status})" for o in orders])
            return context

    @trace_llm_call(model_name="gemini-flash", agent_name="RAG-Engine")
    async def generate_response_async(self, customer_id: str, query: str) -> str:
        """Main entry point with concurrent data fetching"""
        # Fetch knowledge and customer data in parallel
        knowledge_task = asyncio.create_task(asyncio.to_thread(self._cached_knowledge_search, query))
        customer_task = asyncio.create_task(self.get_customer_context_async(customer_id))
        
        knowledge, customer_data = await asyncio.gather(knowledge_task, customer_task)
        
        prompt = f"Context: {knowledge}\nCustomer: {customer_data}\nQuery: {query}\n\nAnswer concisely:"
        
        # Async LLM Call
        response = await self.model.generate_content_async(prompt)
        return response.text

rag_engine = OptimizedRAGEngine()
