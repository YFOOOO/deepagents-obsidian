"""
FastAPI Server for Obsidian AI Assistant Plugin

Provides HTTP REST API endpoints for the TypeScript plugin to communicate
with the DeepAgents-powered Python backend.

Endpoints:
- GET  /health       - Health check
- POST /query        - Process user queries
- GET  /models       - List available models
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Obsidian Assistant
try:
    from obsidian_assistant import create_obsidian_assistant_v2
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from obsidian_assistant import create_obsidian_assistant_v2

app = FastAPI(
    title="Obsidian AI Assistant API",
    description="API server for Obsidian AI Assistant plugin",
    version="0.1.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["app://obsidian.md", "capacitor://localhost", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global assistant instance
assistant = None
OBSIDIAN_PATH = os.getenv(
    "OBSIDIAN_PATH",
    "/Users/yf/Documents/obsidian agent"
)


class QueryRequest(BaseModel):
    query: str
    model: Optional[str] = "qwen-turbo"
    enable_cache: Optional[bool] = True
    enable_smart_routing: Optional[bool] = True
    enable_model_adapter: Optional[bool] = True


class Source(BaseModel):
    title: str
    path: Optional[str] = None
    url: Optional[str] = None
    relevance: float = 0.0


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    route_strategy: Optional[str] = None
    route_coverage: Optional[float] = None
    time_sensitive: Optional[bool] = None
    token_usage: Optional[TokenUsage] = None
    cache_hit: Optional[bool] = False
    error: Optional[str] = None


def initialize_assistant(
    model: str = "qwen-turbo",
    enable_cache: bool = True,
    enable_smart_routing: bool = True,
    enable_model_adapter: bool = True
):
    """Initialize or reinitialize the assistant with given settings."""
    global assistant
    
    print(f"🔧 Initializing assistant with settings:")
    print(f"   - Model: {model}")
    print(f"   - Cache: {enable_cache}")
    print(f"   - Smart Routing: {enable_smart_routing}")
    print(f"   - Model Adapter: {enable_model_adapter}")
    print(f"   - Obsidian Path: {OBSIDIAN_PATH}")
    
    assistant = create_obsidian_assistant_v2(
        docs_path=OBSIDIAN_PATH,
        model_name=model,
        enable_cache=enable_cache,
        enable_smart_routing=enable_smart_routing,
        enable_model_adapter=enable_model_adapter,
        verbose=False
    )
    
    print("✅ Assistant initialized successfully")


@app.on_event("startup")
async def startup_event():
    """Initialize assistant on server startup."""
    print("🚀 Starting Obsidian AI Assistant API Server...")
    initialize_assistant()
    print(f"📍 Server ready at http://localhost:8000")
    print(f"📖 API docs at http://localhost:8000/docs")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "assistant_initialized": assistant is not None,
        "obsidian_path": OBSIDIAN_PATH,
        "obsidian_path_exists": Path(OBSIDIAN_PATH).exists()
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a user query and return AI-generated response."""
    global assistant
    
    if not assistant:
        raise HTTPException(status_code=500, detail="Assistant not initialized")
    
    try:
        # Log query start
        print(f"\n{'='*60}")
        print(f"📝 查询请求: {request.query[:100]}{'...' if len(request.query) > 100 else ''}")
        print(f"{'='*60}")
        
        # Invoke the assistant
        result = assistant.invoke({
            "messages": [("user", request.query)]
        })
        
        # Extract answer
        answer = result.get("answer", "")
        if not answer:
            # Fallback: extract from messages
            messages = result.get("messages", [])
            for msg in reversed(messages):
                if hasattr(msg, "content") and msg.content:
                    answer = msg.content
                    break
        
        # Extract sources
        sources = []
        for source in result.get("sources", []):
            # Handle internal links (from [[path|display]])
            if source.get("type") == "internal":
                sources.append(Source(
                    title=source.get("display", source.get("path", "")),
                    path=source.get("path"),
                    relevance=1.0
                ))
            # Handle external links (from [text](url))
            elif source.get("type") == "external":
                sources.append(Source(
                    title=source.get("text", ""),
                    url=source.get("url"),
                    relevance=1.0
                ))
            # Fallback for other source formats
            else:
                sources.append(Source(
                    title=source.get("title", source.get("display", "")),
                    path=source.get("path"),
                    url=source.get("url"),
                    relevance=source.get("relevance", 0.0)
                ))
        
        # Extract token usage
        token_usage = None
        usage_data = result.get("token_usage")
        if usage_data and isinstance(usage_data, dict):
            token_usage = TokenUsage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0),
                cost=usage_data.get("cost", 0.0)
            )
        
        # Log query completion with statistics
        print(f"\n{'='*60}")
        print(f"✅ 查询完成")
        print(f"{'-'*60}")
        
        # Log route strategy if available
        if result.get("route_strategy"):
            print(f"🧭 路由策略: {result.get('route_strategy')}")
            if result.get("route_coverage") is not None:
                print(f"📊 覆盖率: {result.get('route_coverage'):.1%}")
            if result.get("time_sensitive"):
                print(f"⏰ 时效性: {result.get('time_sensitive')}")
        
        # Log cache status
        if result.get("cache_hit"):
            print(f"⚡ 缓存命中: 是")
        
        # Log token usage
        if token_usage:
            print(f"🔢 Token 使用:")
            print(f"   - Prompt: {token_usage.prompt_tokens:,} tokens")
            print(f"   - Completion: {token_usage.completion_tokens:,} tokens")
            print(f"   - Total: {token_usage.total_tokens:,} tokens")
            print(f"   - Cost: ¥{token_usage.cost:.6f}")
        
        # Log sources count
        print(f"📚 参考来源: {len(sources)} 个")
        print(f"{'='*60}\n")
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            route_strategy=result.get("route_strategy"),
            route_coverage=result.get("route_coverage"),
            time_sensitive=result.get("time_sensitive"),
            token_usage=token_usage,
            cache_hit=result.get("cache_hit", False)
        )
        
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        import traceback
        traceback.print_exc()
        
        return QueryResponse(
            answer="",
            sources=[],
            error=str(e)
        )


@app.get("/models")
async def list_models():
    """List available AI models."""
    try:
        from token_counter import MODEL_PRICING
    except ImportError:
        # Fallback to package import
        try:
            from obsidian_assistant.token_counter import MODEL_PRICING
        except ImportError:
            # If all else fails, return a basic model list
            return {
                "models": [
                    {
                        "name": "qwen-turbo",
                        "display_name": "Qwen Turbo",
                        "input_price": 0.0003,
                        "output_price": 0.0006,
                        "description": "Fast and cost-effective model"
                    }
                ],
                "primary_model": "qwen-turbo"
            }
    
    models = []
    for model_name, pricing in MODEL_PRICING.items():
        models.append({
            "name": model_name,
            "display_name": model_name,
            "input_price": pricing["input"],
            "output_price": pricing["output"],
            "description": pricing.get("description", "")
        })
    
    # Return with primary model
    return {
        "models": models,
        "primary_model": "qwen-turbo"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Check environment variables
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️  Warning: DASHSCOPE_API_KEY not set")
    
    if not os.getenv("TAVILY_API_KEY"):
        print("⚠️  Warning: TAVILY_API_KEY not set (web search will not work)")
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
