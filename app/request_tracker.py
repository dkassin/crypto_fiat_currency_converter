from datetime import datetime, timezone

request_log = {}

def log_request(api_key: str, params: dict, response_body: dict):
    today = datetime.now(timezone.utc).date()

    if api_key not in request_log:
        request_log[api_key] = {}
    
    if today not in request_log[api_key]:
        request_log[api_key][today] = {
            "count": 0,
            "requests": []
        }
    
    request_log[api_key][today]["count"] += 1
    request_log[api_key][today]["requests"].append({
        "timestamp": datetime.now(timezone.utc),
        "params": params,
        "response": response_body
    })

def get_request_count(api_key: str):
    today = datetime.now(timezone.utc).date()

    if api_key in request_log and today in request_log[api_key]:
        return request_log[api_key][today]["count"]
    return 0