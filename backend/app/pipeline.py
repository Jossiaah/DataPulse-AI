import os
import asyncio
import psycopg2
from dotenv import load_dotenv
from anthropic import Anthropic
from openai import OpenAI

# Load enterprise environment parameters from disk
load_dotenv()

async def process_workforce_compliance():
    print("🤖 Initializing AI Solutions Compliance Pipeline Engine...")
    
    # Connect directly to your running PostgreSQL container
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "datapulse_admin"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "datapulse_warehouse")
    )
    cursor = conn.cursor()
    
    # Ingest the raw data rows out of your database storage layer
    cursor.execute("SELECT employee_name, department, assigned_hours, shift_notes FROM raw_workforce_logs;")
    records = cursor.fetchall()
    
    # Initialize the AI Client (Uses Anthropic Claude as a baseline, falls back to OpenAI)
    if os.getenv("ANTHROPIC_API_KEY"):
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        ai_provider = "anthropic"
    else:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        ai_provider = "openai"
        
    print(f"📡 Securely linked to AI Provider: {ai_provider.upper()}\n")

    for record in records:
        name, dept, hours, notes = record
        print(f"📋 Analyzing logs for Employee: {name} ({dept})")
        
        # Design a structured systemic prompt to enforce compliance logic evaluation
        prompt = f"""
        You are an elite enterprise operations compliance auditor. Evaluate the following employee log row for shift overages, burnout risks, or credential gaps.
        
        Employee Name: {name}
        Department: {dept}
        Assigned Hours: {hours}
        Shift Notes: {notes}
        
        Provide a concise, 2-sentence structural safety evaluation. If an anomaly or risk is detected, clearly start your response with '[CRITICAL WARNING]'. If clear, start with '[PASSED]'.
        """
        
        # Dispatch the payload asynchronously to the AI API endpoints
        try:
            if ai_provider == "anthropic":
                response = client.messages.create(
                    model="claude-fable-5",
                    max_tokens=150,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Dynamic block extraction to safely ignore internal ThinkingBlocks
                analysis = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        analysis = block.text
                        break
            else:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    max_tokens=150,
                    messages=[{"role": "user", "content": prompt}]
                )
                analysis = response.choices.message.content
                
            print(f"🤖 AI Analysis Result:\n{analysis.strip()}\n")
            
        except Exception as e:
            print(f"⚠️ Query Error encountered on {name}: {str(e)}")
        
    cursor.close()
    conn.close()

if __name__ == "__main__":
    asyncio.run(process_workforce_compliance())
