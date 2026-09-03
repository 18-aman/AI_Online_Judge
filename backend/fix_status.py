with open('app/services/judge.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_wait = '''                try:
                    container.wait(timeout=10) # Generous overhead for compilation/Docker boot
                    logs = container.logs()
                    logs = logs.decode("utf-8").strip() if isinstance(logs, bytes) else logs.strip()
                    
                    # Check for runtime errors'''

new_wait = '''                try:
                    wait_res = container.wait(timeout=10) # Generous overhead for compilation/Docker boot
                    exit_code = wait_res.get("StatusCode", 0)
                    
                    logs = container.logs()
                    logs = logs.decode("utf-8").strip() if isinstance(logs, bytes) else logs.strip()
                    
                    if exit_code == 124:
                        results.append({"id": str(tc.id), "status": "Time Limit Exceeded", "error": "Execution exceeded the time limit."})
                        continue

                    # Check for runtime errors'''

content = content.replace(old_wait, new_wait)

with open('app/services/judge.py', 'w', encoding='utf-8') as f:
    f.write(content)
