# Exec vs Attach to detached Container

Yes: when you run

```bash
docker exec -it mybox bash
```

→ you're spawning a **new process** inside the container.

It is **not** PID 1. It’s a **child** of PID 1 (or even a sibling depending on the init system).

---

## 🚫 Can you `exec` *into* PID 1 directly?

**Short answer: No—not in the same way.**

`docker exec` *always* spawns a new process.

Why? Because Docker isn’t "attaching" you to an existing process—it’s creating a fresh one inside the container’s namespace.

---

## 🧠 So how *can* you interact with PID 1?

### ✅ Option 1: `docker attach`

```bash
docker attach mybox
```

- This attaches your terminal to whatever PID 1 is running
- If PID 1 is `bash`, you’re now "in" the original bash process

**BUT WARNING:**

- If you type `exit`, you **kill** PID 1 → container dies
- `attach` gives you **no buffer** between your input and PID 1's life

This is the **closest you can get** to truly entering the original shell.

---

### ✅ Option 2: Run with a terminal multiplexer (e.g. `tmux` or `screen`)

Run the container like this:

```bash
docker run -dit --name tmuxbox ubuntu bash
```

Then:

```bash
docker exec -it tmuxbox bash
apt update && apt install -y tmux
tmux
```

Now PID 1 can be `tmux` instead of `bash`, or it can spawn `tmux` early.

Then you can attach to the same session multiple ways:

```bash
docker exec -it tmuxbox tmux attach
```

→ This gives you shared access to the **same shell session**, if that’s the goal.

---

### ✅ Option 3: Inspect and signal PID 1

```bash
bash
CopyEdit
docker exec mybox ps aux

```

Find PID 1. Then:

```bash
docker exec mybox strace -p 1
```

→ You can inspect its syscalls.

But you **can’t `exec` into it**, because processes aren’t composable like threads.

---

## 🔍 Summary

| Goal | Doable? | Method |
| --- | --- | --- |
| Attach to PID 1 (`bash`) directly | ✅ | `docker attach mybox` |
| Exec into PID 1 | ❌ | Not possible—only spawn new |
| Share terminal with PID 1 | ✅ | Use `tmux`, `screen`, or FIFO |
| Inspect PID 1 | ✅ | `ps`, `strace`, `/proc/1` |

---

## 🧠 Final Thought

Think of Docker containers like **namespaces + PID 1 lifeline**:

You can **exec into the namespace**, but you can’t *become* another process—you can only run *beside* it.

Want to explore `/proc/1`, see how namespaces differ, or try bu