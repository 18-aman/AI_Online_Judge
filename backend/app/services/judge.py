import docker
import tempfile
import os
import time
from typing import List, Dict, Any
from app.models.problem import TestCase
from app.services.generator import generate_executable_wrapper

DOCKER_IMAGES = {
    "python": "python:3.9-slim",
    "cpp": "gcc:latest",
    "java": "eclipse-temurin:17-jdk-jammy"
}

def run_code_in_docker(language: str, code: str, test_cases: List[TestCase], time_limit: float, custom_checker_code: str = None, signature_schema: dict = None) -> Dict[str, Any]:
    client = docker.from_env()
    image = DOCKER_IMAGES.get(language)
    
    if not image:
        return {"status": "Error", "message": f"Unsupported language: {language}"}

    wrapped_code = generate_executable_wrapper(signature_schema, language, code)

    
    # Ensure image exists
    try:
        client.images.get(image)
    except docker.errors.ImageNotFound:
        client.images.pull(image)

    results = []
    
    for tc in test_cases:
        with tempfile.TemporaryDirectory() as temp_dir:
            if language == "python":
                file_name = "solution.py"
                command = f"python {file_name}"
            elif language == "cpp":
                file_name = "solution.cpp"
                # Compile and then run
                command = f"sh -c 'g++ {file_name} -o solution && ./solution'"
            elif language == "java":
                file_name = "Main.java"
                command = f"sh -c 'javac Main.java && java Main'"
            
            file_path = os.path.join(temp_dir, file_name)
            with open(file_path, "w", newline="\n", encoding="utf-8") as f:
                f.write(wrapped_code)
                
            try:
                input_file_path = os.path.join(temp_dir, "input.txt")
                with open(input_file_path, "w", newline="\n", encoding="utf-8") as f:
                    f.write(tc.input_data)
                    
                if language == "python":
                    run_cmd = f"sh -c 'timeout {time_limit} python {file_name} < input.txt'"
                elif language == "cpp":
                    run_cmd = f"sh -c 'g++ {file_name} -o solution && timeout {time_limit} ./solution < input.txt'"
                elif language == "java":
                    run_cmd = f"sh -c 'javac Main.java && timeout {time_limit} java Main < input.txt'"

                container = client.containers.run(
                    image,
                    command=run_cmd,
                    volumes={temp_dir: {'bind': '/app', 'mode': 'rw'}},
                    working_dir='/app',
                    mem_limit="256m",
                    network_disabled=True,
                    detach=True
                )
                
                try:
                    wait_res = container.wait(timeout=10) # Generous overhead for compilation/Docker boot
                    exit_code = wait_res.get("StatusCode", 0)
                    
                    logs = container.logs()
                    logs = logs.decode("utf-8").strip() if isinstance(logs, bytes) else logs.strip()
                    
                    if exit_code == 124:
                        results.append({"id": str(tc.id), "status": "Time Limit Exceeded", "error": "Execution exceeded the time limit."})
                        continue

                    # Check for runtime errors
                    if "Traceback" in logs or "Exception" in logs or "terminate called" in logs:
                        results.append({"id": str(tc.id), "status": "Runtime Error", "error": logs})
                    else:
                        if custom_checker_code:
                            try:
                                # Safely execute the custom checker in a sandboxed namespace
                                checker_env = {}
                                exec(custom_checker_code, checker_env)
                                
                                # The checker must define `def check(input_data: str, user_output: str) -> bool:`
                                if "check" not in checker_env:
                                    results.append({"id": str(tc.id), "status": "Error", "message": "Custom checker must define a 'check' function."})
                                else:
                                    is_correct = checker_env["check"](tc.input_data, logs)
                                    if is_correct:
                                        results.append({"id": str(tc.id), "status": "Accepted", "output": logs})
                                    else:
                                        results.append({"id": str(tc.id), "status": "Wrong Answer", "output": logs, "expected": tc.expected_output})
                            except Exception as e:
                                results.append({"id": str(tc.id), "status": "Error", "message": f"Custom Checker Error: {str(e)}"})
                        else:
                            # Standard strict text matching
                            if logs == (tc.expected_output or "").strip():
                                results.append({"id": str(tc.id), "status": "Accepted", "output": logs})
                            else:
                                results.append({"id": str(tc.id), "status": "Wrong Answer", "output": logs, "expected": tc.expected_output})
                    
                except Exception as e:
                    # Timeout or execution error
                    results.append({"id": str(tc.id), "status": "Time Limit Exceeded or Error"})
                finally:
                    container.remove(force=True)
                    
            except Exception as e:
                results.append({"id": str(tc.id), "status": "Runtime Error", "error": str(e)})

    # Determine overall verdict
    overall_status = "Accepted"
    for r in results:
        if r["status"] != "Accepted":
            overall_status = r["status"]
            break
            
    return {
        "status": overall_status,
        "results": results
    }
