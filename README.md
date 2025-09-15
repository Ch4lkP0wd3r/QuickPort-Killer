# ⚡ QuickPort-Killer
> Kill processes by port — safe, fast, hacker-approved.  
> Built with ❤️ by **Ch4lkP0wd3r**

![Python](https://img.shields.io/badge/python-3.7%2B-blue) 
![License](https://img.shields.io/badge/license-MIT-green) 
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows-lightgrey)

---

##  Problem

You’re coding, spin up a server, and suddenly:  
```
Error: Address already in use
```
Some zombie process is camping on your port like it owns the place.  

You could wrestle with `lsof`, `netstat`, or Task Manager…  
Or just free your port instantly.   

---

## 💡 Solution: QuickPort-Killer

A Python tool to:

-  Identify the process hogging your port  
-  Kill it safely (or brutally, if needed)  
-  Avoid nuking critical services (like `systemd` or `explorer.exe`)  
-  List active ports in plain text or JSON  
-  Handle multiple ports at once  

---

## 🚀 Installation

Clone the repo:

```bash
git clone https://github.com/YOUR-USERNAME/QuickPort-Killer.git
cd QuickPort-Killer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Usage

```bash
# Kill the process on port 3000
python quickportkiller.py 3000

# Kill multiple ports
python quickportkiller.py --ports 8080 5000 1337

# List all busy ports
python quickportkiller.py --list

# List in JSON format
python quickportkiller.py --list --json

# Force kill (override safety checks)
python quickportkiller.py 22 --force
```

---

## ⚠️ Safety Features

✔️ Blocks killing of critical ports (`22`, `80`, `443`, `3306`, etc.) unless `--force` is used  
✔️ Protects processes like `systemd`, `explorer.exe`, `lsass.exe`  
✔️ Prompts before termination (unless forced)  

---

## 📦 Requirements

- Python **3.7+**  
- [psutil](https://pypi.org/project/psutil/)  

Install with:

```bash
pip install -r requirements.txt
```

---

##  Example Output

```bash
$ python quickportkiller.py --list

Active ports:
Port 3000 → PID 4521 (node)
Port 8080 → PID 9214 (python3)
Port 22   → PID 1 (systemd)
```

---

## 📜 License

MIT License — use, hack, share.  
⚠️ If you blow up your system, that’s on you. 😉

---

## ✨ Credits

Created by **Ch4lkP0wd3r** 🐾  
Because life’s too short to hunt ports manually. ;)

