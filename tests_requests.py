import requests

print("✅ Requests library is successfully installed!")
print(f"Version: {requests.__version__}")

# Test a simple request
try:
    response = requests.get("https://httpbin.org/json", timeout=5)
    print(f"✅ Test request successful! Status code: {response.status_code}")
    print("🎉 Everything is working correctly!")
except Exception as e:
    print(f"❌ Test request failed: {e}")