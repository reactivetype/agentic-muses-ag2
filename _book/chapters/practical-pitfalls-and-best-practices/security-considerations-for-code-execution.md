# Security Considerations for Code Execution

Security is paramount when executing code in agent systems.

## Related Concepts

- [Error Handling](./error-handling-in-agent-orchestration.html)
- [Testing and Logging](./testing-and-logging-strategies.html)
- [Advanced Agent Orchestration](../advanced-agent-orchestration/README.html)
- [Context Variables](../context-variables-and-conditional-logic/contextvariables.html)
- [State Management](../context-variables-and-conditional-logic/StateManagement.html)

## Overview

When building multi-agent systems that execute code—whether running user-generated scripts, invoking APIs, or using external tools—security becomes a critical concern. Unrestricted code execution can expose your system to attacks such as code injection, privilege escalation, data leakage, and denial of service. This chapter addresses common security pitfalls and presents best practices for securely handling code execution in agent workflows.

---

## Explanation

### Why is Code Execution Risky?

Multi-agent systems often automate complex workflows, sometimes allowing dynamic or user-supplied code execution. Without proper safeguards, this can lead to:

- **Unauthorized Access:** Malicious code could access sensitive files or data.
- **System Compromise:** Attackers may exploit vulnerabilities to gain control over the host system.
- **Resource Exhaustion:** Poorly written or malicious scripts can consume excessive CPU, memory, or disk resources.
- **Data Leakage:** Sensitive information may be inadvertently exposed to unauthorized parties.

### Key Attack Vectors

1. **Code Injection:** Unsanitized input leads to execution of unintended commands.
2. **Insecure Dependencies:** Third-party libraries or tools may introduce vulnerabilities.
3. **Improper Permissions:** Running agents with excessive privileges increases risk.
4. **Lack of Monitoring:** Without logging, attacks or misuse can go undetected.

### Example Scenario

Suppose an agent accepts Python code snippets to automate data analysis. If user input isn't properly validated, an attacker could submit:

```python
import os
os.system('rm -rf /')
```

If executed as-is, this command could delete critical system files.

---

## Examples

### Example 1: Unsafe Code Execution

**Bad Practice:**

```python
# Dangerous: Directly executing user-supplied code
user_code = input("Enter Python code: ")
exec(user_code)  # Do not use!
```

**Risks:**
- Arbitrary code execution
- Data exfiltration or system compromise

---

### Example 2: Safer Code Execution with Sandboxing

**Better Practice:**

```python
import subprocess

def safe_run_script(code: str):
    # Write code to a temporary file
    with open('/tmp/user_code.py', 'w') as f:
        f.write(code)
    # Execute in a restricted subprocess
    result = subprocess.run(
        ['python3', '/tmp/user_code.py'],
        timeout=5,
        capture_output=True,
        check=False
    )
    return result.stdout[-1000:]  # Limit output size

# Example usage
user_code = "print('Hello, world!')"
print(safe_run_script(user_code))
```

**Improvements:**
- Runs code in a separate process
- Timeout limits execution time
- Output size is restricted

---

### Example 3: Using Containers for Isolation

```bash
# Run user code in a Docker container with limited resources and no network access
docker run --rm -m 128m --cpus=0.5 --network=none -v $(pwd)/user_code.py:/usr/src/app/code.py python:3.9 python code.py
```

**Benefits:**
- Limits CPU and memory usage
- Prevents network access
- Provides filesystem isolation

---

## Best Practices

- **Input Validation:** Never execute code or commands from unsanitized input.
- **Principle of Least Privilege:** Run agents and subprocesses with the minimal required permissions. Avoid running as root.
- **Sandboxing:** Execute user code in isolated environments (e.g., containers, VMs, or restricted interpreters).
- **Resource Limiting:** Set strict timeouts, memory, and CPU limits for code execution.
- **Dependency Management:** Use trusted libraries and monitor for security updates.
- **Logging and Monitoring:** Log all code executions, inputs, and outputs. Monitor for unusual behavior or resource usage.
- **Disable Dangerous Functions:** Restrict or sandbox access to filesystem, system calls, and network functions where possible.
- **Regular Audits:** Review code and configurations regularly for security issues.
- **Error Handling:** Never expose stack traces or sensitive error information to untrusted users.

### Common Pitfalls

- Directly using `eval` or `exec` on user input
- Running code with administrator privileges
- Ignoring failed subprocesses or missing timeouts
- Omitting audit logs for executed code

---

By following these guidelines, you can significantly reduce the risks associated with code execution in multi-agent workflows and build more secure and resilient systems.