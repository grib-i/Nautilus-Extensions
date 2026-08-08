# Nautilus-Extensions

A lightweight Python extension for the Nautilus file manager (GNOME) that restores the missing "Create File" item directly in the right-click (PKM) context menu.

## Installing

### 1. Install dependencies

Choose the command for your Linux distribution:

- **Ubuntu / Debian / Pop!\_OS:**

  ```bash
  sudo apt install python3-nautilus gir1.2-adw-1
  ```

- **Fedora / RHEL:**

  ```bash
  sudo dnf install nautilus-python libadwaita
  ```

- **Arch Linux / Manjaro:**
  ```bash
  sudo pacman -S python-nautilus libadwaita
  ```

### 2. Clone & Install

Run these commands in your terminal to clone the repository and run the installer:

```bash
git clone https://github.com && cd Nautilus-Extensions
```

```bash
chmod +x install.sh
```

```bash
./install.sh
```

## About

GNOME removed the simple "New File" option from the root context menu. This extension fixes that behavior cleanly, without adding heavy background processes or unnecessary features.
