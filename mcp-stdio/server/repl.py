import subprocess
from pathlib import Path

CONTAINER = "shared-box"
SANDBOX_DIR = "/home/sandbox"

def run_in_container(command: str, workdir: str = "/"):
    result = subprocess.run(
        ["docker", "exec", CONTAINER, "bash", "-c", f"cd {workdir} && {command}"],
        capture_output=True,
        text=True
    )
    return result

def main():
    print(f"Connected to container: {CONTAINER}")
    print("Type 'exit' to quit.\n")
    
    # initialize sandbox directory
    run_in_container(f"mkdir -p {SANDBOX_DIR}")

    while True:
        try:
            cmd = input(">> ").strip()
            if not cmd:
                continue
            if cmd.lower() in ("exit", "quit"):
                break

            result = run_in_container(cmd)
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(result.stderr.strip(), file=sys.stderr)

            # print(f"[exit code: {result.returncode}]\n")

        except KeyboardInterrupt:
            print("\nInterrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"[error: {e}]")

if __name__ == "__main__":
    import sys
    main()
