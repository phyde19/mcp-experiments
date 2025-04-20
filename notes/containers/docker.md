# Docker

[install docker guide](https://www.linux.org/threads/docker-basics-and-install.21840/)

## 🔧 0. Goal-Oriented Agenda

You'll learn:

1. ✅ How to install Docker on **Fedora**
2. ✅ How to control the **Docker daemon**
3. ✅ Where everything lives on **disk**
4. ✅ Command suite for managing **images**, **containers**, and **system**
5. ✅ How to run a **Hello World** and then drop into a **Bash shell inside a container**

Let’s go step by step.

---s

## 📦 1. Install Docker on Fedora

Fedora doesn’t ship with Docker CE anymore due to a philosophical split, but you can still install it cleanly from Docker’s own repo.

### 🔹 Step-by-step:

```bash
bash
CopyEdit
# Remove old versions if they exist
sudo dnf remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

# Add the Docker repo
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# Install Docker
sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start and enable the Docker daemon
sudo systemctl start docker
sudo systemctl enable docker

# (Optional) Add yourself to the docker group
sudo usermod -aG docker $USER

```

👉 Log out and back in (or `newgrp docker`) to avoid needing `sudo docker`.

---

## 🧠 2. Docker Daemon: Control It

```bash
bash
CopyEdit
# Start the Docker daemon
sudo systemctl start docker

# Enable it at boot
sudo systemctl enable docker

# Check its status
sudo systemctl status docker

# Restart it (e.g. after config changes)
sudo systemctl restart docker

# Stop it
sudo systemctl stop docker

```

---

## 📁 3. Key File Paths

| Path | Purpose |
| --- | --- |
| `/var/lib/docker` | Default storage for images, containers, etc. |
| `/etc/docker/daemon.json` | Daemon configuration (e.g. default options) |
| `/run/docker.sock` | Unix socket for Docker CLI <-> daemon |
| `/var/run/docker.pid` | PID of Docker daemon |
| `/etc/systemd/system/docker.service` | Daemon unit (if you want to inspect) |

You can run this to explore the live filesystem state:

```bash
sudo tree -L 2 /var/lib/docker

```

---

## 🧪 4. Suite of Docker Commands

### 🔹 Images

```bash
bash
CopyEdit
docker pull ubuntu                         # Fetch image
docker images                              # List local images
docker rmi IMAGE_ID                        # Remove image

```

### 🔹 Containers

```bash
bash
CopyEdit
docker run hello-world                     # Hello world test
docker ps                                  # List running containers
docker ps -a                               # All containers (including exited)
docker stop CONTAINER_ID                   # Stop container
docker start CONTAINER_ID                  # Start a stopped container
docker rm CONTAINER_ID                     # Remove stopped container

```

### 🔹 Other useful

```bash
bash
CopyEdit
docker logs CONTAINER_ID                   # See logs of container
docker exec -it CONTAINER_ID bash          # Run bash in live container
docker inspect CONTAINER_ID                # Deep JSON info
docker system df                           # Disk usage summary
docker system prune                        # Clean up stopped containers, networks, etc.

```

---

## 👋 5. Hello World: First Container

```bash
bash
CopyEdit
docker run hello-world

```

Expected output:

```
css
CopyEdit
Hello from Docker!
This message shows that your installation appears to be working correctly.
...

```

---

## 🧰 6. Run a Bash Shell in a Container

This spins up a **temporary Ubuntu container** and gives you a shell inside it:

```bash
bash
CopyEdit
docker run -it --rm ubuntu bash

```

- `it`: interactive + TTY
- `-rm`: auto-remove when done
- `ubuntu`: use Ubuntu image
- `bash`: run `bash` as the container's entry command

You can now explore:

```bash
bash
CopyEdit
ls /
ps aux
cat /etc/os-release

```

Exit with `exit`.

---

## ✅ At This Point You Should Know

- How Docker installs, starts, lives on Fedora
- Where its files and sockets live
- How to spin up and kill containers
- How to explore inside the container

---

Want to do a `strace` on a container next? Or check `/proc` on the host vs container? Or maybe we move to `docker-compose` next?

# 🔧 Manual Repo Setup (Workaround)

Instead of relying on `--add-repo`, do this:

### 🧱 Step 1: Create the Docker repo file

```bash
sudo tee /etc/yum.repos.d/docker-ce.repo > /dev/null <<EOF
[docker-ce-stable]
name=Docker CE Stable - \$basearch
baseurl=https://download.docker.com/linux/fedora/\$releasever/\$basearch/stable
enabled=1
gpgcheck=1
gpgkey=https://download.docker.com/linux/fedora/gpg
EOF

```

### 🧪 Step 2: Verify it's visible

```bash
dnf repolist | grep docker
```

Should show: `docker-ce-stable`.


🚦 start vs enable — Deep Cut

Command	What it does	When it runs
sudo systemctl start docker	Starts the service now	Immediate
sudo systemctl enable docker	Enables the service to start on boot	At every system reboot onward
