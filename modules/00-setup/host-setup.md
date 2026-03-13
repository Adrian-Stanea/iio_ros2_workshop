# Host Setup (Windows)

This guide covers setting up your Windows development environment for the workshop.

## 1. Install WSL2

Windows Subsystem for Linux 2 provides the Linux environment needed for Docker.

1. Open PowerShell as Administrator
2. Run: `wsl --install`
3. Restart your computer when prompted

> **Reference:** [Microsoft WSL Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install)

**Verify:**
```powershell
wsl --version
```

## 2. Install Docker Desktop

Docker Desktop manages containers and integrates with WSL2.

1. Download from [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
2. Run installer
3. During setup, ensure "Use WSL 2 instead of Hyper-V" is selected
4. Restart if prompted

**Verify:**
```powershell
docker --version
```

> **Note:** The command should work from but PowerShell and WSL2 terminal.

## 3. Install VS Code with Dev Containers

VS Code with the Dev Containers extension provides the development environment.

1. Download from [VS Code](https://code.visualstudio.com/)
2. Install VS Code
3. Open VS Code
4. Go to Extensions (Ctrl+Shift+X)
5. Search for "Dev Containers"
6. Install "Dev Containers" by Microsoft (ms-vscode-remote.remote-containers)

**Verify:** Extension appears in the Extensions sidebar

## 4. Install Scopy (Windows)

Scopy controls the M2K device for signal generation.

1. Download from [Scopy Download Page](https://github.com/analogdevicesinc/scopy/releases)
2. Run installer
3. Connect M2K via USB
4. Launch Scopy

**Verify:** Scopy opens and shows "M2K" in device list

## 5. Clone Repository

From WSL2 terminal, run:

```bash
git clone https://github.com/Adrian-Stanea/iio_ros2_workshop
cd iio_ros2_workshop
```

## Next Steps

Proceed to [RPi5 Setup](rpi5-setup.md)
