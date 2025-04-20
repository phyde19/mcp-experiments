# Running Commands From Python 

## 🐍 Now enter Python’s `subprocess`

In Python, if you use:

```python
subprocess.run("echo $HOME", shell=True)
```

- Python spawns a shell (`/bin/sh`)
- `$HOME` gets expanded **by the shell**
- Quotes behave *as the shell interprets them*

So if you do:

```python
subprocess.run("echo '$HOME'", shell=True)
```

It prints literally `$HOME`, because **single quotes** protect it.

---

## ✅ Recommendation when writing Python wrappers

When calling `subprocess.run`:

### 🔹 Option 1: Shell commands (use `shell=True` + quote like Bash)

```python
subprocess.run("docker exec shared-box bash -c 'echo \"hello $HOME\"'", shell=True)
```

- Bash will expand `$HOME` **inside the container** if it's defined
- Double quotes **inside** single quotes = safe shell string

### 🔹 Option 2: Programmatic args (use list form, no shell)

```python
subprocess.run([
    "docker", "exec", "shared-box", "bash", "-c", "echo 'hello docker'"
])
```

- No need to quote anything manually
- No shell parsing at all; arguments are passed as-is
- **This is safer** if you control the arguments

---

## ✅ TL;DR Ruleset

| Language | Quote `"` vs `'` matters? | Notes |
| --- | --- | --- |
| Bash CLI | ✅ Yes | `'...'` = literal; `"..."` = interpolate |
| Python string | ✅ Yes | Just normal Python string rules |
| Python subprocess with `shell=True` | ✅ Yes | Shell rules apply (same as Bash) |
| Python subprocess with list args | ❌ No | Shell not involved; quoting is not interpreted |

---

Want me to show you how to safely implement your `say_hello()` wrapper in Python that takes arbitrary shell logic and runs it inside a container with proper quoting?