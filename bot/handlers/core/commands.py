import httpx
import config

def get_client():
    return httpx.Client(timeout=5, trust_env=False, headers={"Authorization": f"Bearer {config.LMS_API_KEY}"})

def handle_start():
    return "Welcome! I am your LMS bot. Use /help to see available commands."

def handle_help():
    return """Available commands:
/start - Welcome message
/help - List all commands
/health - Check backend status
/labs - List available labs
/scores <lab> - Show pass rates for a lab"""

def handle_health():
    try:
        with get_client() as client:
            resp = client.get(f"{config.LMS_API_BASE_URL}/items/")
            resp.raise_for_status()
            return f"Backend is healthy. {len(resp.json())} items available."
    except Exception as e:
        return f"Backend error: {str(e)}"

def handle_labs():
    try:
        with get_client() as client:
            resp = client.get(f"{config.LMS_API_BASE_URL}/items/")
            resp.raise_for_status()
            data = resp.json()
            labs = [i.get('title') for i in data if i.get('type') == 'lab' or 'Lab' in str(i.get('title'))]
            if not labs: return "No labs available."
            # Используем set(), чтобы убрать дубликаты "Lab setup"
            unique_labs = sorted(list(set(labs)))
            return "Available labs:\n" + "\n".join([f"- {lab}" for lab in unique_labs])
    except Exception as e:
        return f"Backend error: {str(e)}"

def handle_scores(args):
    if not args:
        return "Please provide a lab name. Example: /scores lab-04"
    lab_id = args.strip()
    try:
        with get_client() as client:
            resp = client.get(f"{config.LMS_API_BASE_URL}/analytics/pass-rates?lab={lab_id}")
            resp.raise_for_status()
            data = resp.json()
            if not data: return f"No pass rates found for {lab_id}."
            
            res = [f"Pass rates for {lab_id}:"]
            for item in data:
                # Ищем название задачи в разных полях
                name = item.get('task') or item.get('task_name') or item.get('title') or item.get('task_id') or "Unknown Task"
                
                rate = item.get('pass_rate', 0.0)
                attempts = item.get('total_attempts', 0)
                
                # Форматируем проценты (0.92 -> 92.0%)
                if isinstance(rate, (int, float)) and 0 < rate <= 1.0:
                    rate_val = f"{rate * 100:.1f}%"
                else:
                    rate_val = f"{rate}%"
                
                res.append(f"- {name}: {rate_val} ({attempts} attempts)")
            return "\n".join(res)
    except Exception as e:
        return f"Backend error: {str(e)}"
