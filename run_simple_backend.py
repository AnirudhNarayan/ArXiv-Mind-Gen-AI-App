#!/usr/bin/env python3
"""
Simple Backend Runner
Start the simplified ArxivMind backend
"""

import os
import sys
import uvicorn

def main():
    """Start the simple backend server"""
    print("🚀 Starting ArxivMind Simple Backend...")
    print("📊 Using cost-optimized OpenAI API calls")
    print("💰 Budget limit: $2.00")
    print("-" * 50)
    
    # Set environment variables if needed
    os.environ.setdefault("PYTHONPATH", os.getcwd())
    
    try:
        uvicorn.run(
            "backend.simple_main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


