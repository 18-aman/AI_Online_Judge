with open('app/services/judge.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Python command to use timeout
content = content.replace("run_cmd = f\"sh -c 'python {file_name} < input.txt'\"", "run_cmd = f\"sh -c 'timeout {time_limit} python {file_name} < input.txt'\"")

# Replace C++ command
content = content.replace("run_cmd = f\"sh -c 'g++ {file_name} -o solution && ./solution < input.txt'\"", "run_cmd = f\"sh -c 'g++ {file_name} -o solution && timeout {time_limit} ./solution < input.txt'\"")

# Replace Java command
content = content.replace("run_cmd = f\"sh -c 'javac Main.java && java Main < input.txt'\"", "run_cmd = f\"sh -c 'javac Main.java && timeout {time_limit} java Main < input.txt'\"")

# Replace container.wait(timeout=int(time_limit) + 1)
content = content.replace("container.wait(timeout=int(time_limit) + 1)", "container.wait(timeout=10) # Generous overhead for compilation/Docker boot")

with open('app/services/judge.py', 'w', encoding='utf-8') as f:
    f.write(content)
