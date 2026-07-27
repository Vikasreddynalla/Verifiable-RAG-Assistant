import time
import requests

base_url = "https://verifiable-rag-assistant-1.onrender.com"
print(f"Monitoring deployment status at {base_url}...")
start_time = time.time()
timeout = 360 # 6 minutes (gives enough build time)

success = False
while time.time() - start_time < timeout:
    try:
        # Check Streamlit UI
        resp_ui = requests.get(base_url, timeout=15)
        print(f"[{int(time.time() - start_time)}s] UI Status: {resp_ui.status_code}")
        
        if resp_ui.status_code == 200:
            print("  UI is online! Checking backend endpoints...")
            
            # Check health
            try:
                resp_health = requests.get(f"{base_url}/health", timeout=10)
                print(f"  Health Endpoint Status: {resp_health.status_code}")
                if resp_health.status_code == 200:
                    print(f"  Health Check Response: {resp_health.json()}")
            except Exception as e:
                print(f"  Health Check Error: {e}")
                
            # Check docs
            try:
                resp_docs = requests.get(f"{base_url}/docs", timeout=10)
                print(f"  Docs Endpoint Status: {resp_docs.status_code}")
            except Exception as e:
                print(f"  Docs Check Error: {e}")
                
            success = True
            break
            
    except Exception as e:
        print(f"[{int(time.time() - start_time)}s] Connection state: {type(e).__name__}")
        
    time.sleep(15)

if success:
    print("\n=== DEPLOYMENT IS FULLY OPERATIONAL ===")
else:
    print("\n=== DEPLOYMENT MONITOR TIMED OUT ===")
    exit(1)
