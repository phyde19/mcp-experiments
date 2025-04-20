## 🧠 Canonical Form of `docker run`

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

### 🔹 Where:

- `OPTIONS`: Host-level flags (networking, volumes, ports, etc.)
- `IMAGE`: The container image to use (e.g. `ubuntu`, `node`, `postgres`)
- `COMMAND`: Optional override for the container’s default **entrypoint**
- `ARG...`: Arguments to that command

---

## 🧠 What's Actually Happening?

When you run a container, Docker:

1. **Loads the image**
2. **Creates a container filesystem from that image**
3. **Runs an ENTRYPOINT process inside the container**
4. **OPTIONALLY replaces the default CMD or ENTRYPOINT with what you pass**

## 🧠 Key Principle:
A Docker container lives only as long as its PID 1 process lives.

> That’s it. Full stop.