#!/usr/bin/env python3
"""
QuickPort-Killer: free up ports fast by killing the process
needs: psutil (pip install psutil)
"""

import argparse
import psutil
import sys
import os
import json
import platform

# some ports are system critical
CRITICAL_PORTS = {22, 80, 443, 53, 123, 631, 3306, 5432}

# processes i dont want ppl to kill accidentally
WIN_PROTECTED = {
    "explorer.exe", "wininit.exe", "services.exe",
    "lsass.exe", "csrss.exe", "svchost.exe", "winlogon.exe"
}
NIX_PROTECTED = {
    "systemd", "init", "kthreadd", "ksoftirqd",
    "rcu_sched", "migration", "watchdog", "kworker"
}

def get_protected():
    if platform.system().lower().startswith("win"):
        return WIN_PROTECTED
    return NIX_PROTECTED

def find_by_port(port):
    pids = []
    try:
        for c in psutil.net_connections(kind="inet"):
            if c.laddr.port == port and c.pid:
                pids.append(c.pid)
    except Exception as e:
        print("cant read connections:", e)
        sys.exit(1)
    return list(set(pids))

def list_ports():
    seen = set()
    for c in psutil.net_connections(kind="inet"):
        if c.status == "LISTEN" and c.pid and (c.laddr.port, c.pid) not in seen:
            seen.add((c.laddr.port, c.pid))
            try:
                yield c.laddr.port, c.pid, psutil.Process(c.pid).name()
            except psutil.NoSuchProcess:
                continue

def kill(pid, timeout=3, verbose=False):
    try:
        proc = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return False
    try:
        proc.terminate()
        if verbose: print("sent terminate to", pid)
        proc.wait(timeout=timeout)
        return True
    except psutil.TimeoutExpired:
        if verbose: print("timeout, killing", pid)
        proc.kill()
        return True
    except Exception as e:
        print("fail killing", pid, e)
        return False

def main():
    p = argparse.ArgumentParser(description="kill proc using a port")
    g = p.add_mutually_exclusive_group(required=False)  # Changed to False
    g.add_argument("port", type=int, nargs="?", help="single port")
    g.add_argument("--ports", type=int, nargs="+", help="multi ports")
    p.add_argument("--force", action="store_true", help="skip confirm + safety")
    p.add_argument("--list", action="store_true", help="show busy ports")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--timeout", type=int, default=3)
    p.add_argument("--json", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="dont actually kill")
    args = p.parse_args()

    prot = get_protected()
    out = []

    if args.list:
        if args.json:
            print(json.dumps([{"port": p, "pid": pid, "name": n} for p, pid, n in list_ports()], indent=2))
        else:
            for pnum, pid, name in list_ports():
                print(f"{pnum} -> {pid} ({name})")
        sys.exit(0)

    # Check if we have ports to work with when not listing
    if not args.port and not args.ports:
        p.error("must specify a port or --ports when not using --list")

    ports = args.ports if args.ports else [args.port]
    for port in ports:
        if port in CRITICAL_PORTS and not args.force:
            print("nope, critical port", port, "(use --force)")
            continue
        if port < 1024 and not args.force:
            print("privileged port", port, "(need --force)")
            continue

        pids = find_by_port(port)
        if not pids:
            print("nothing on port", port)
            continue

        for pid in pids:
            if pid == os.getpid():
                print("not killing myself lol")
                continue
            try:
                name = psutil.Process(pid).name()
            except psutil.NoSuchProcess:
                continue

            if name.lower() in (n.lower() for n in prot) and not args.force:
                print("protected proc", name, "skip")
                continue

            if args.dry_run:
                print("[dry] would kill", pid, name, "on", port)
                out.append({"port": port, "pid": pid, "name": name, "status": "would_kill"})
                continue

            if args.force or input(f"kill {pid} ({name}) on {port}? y/n: ").lower() == "y":
                if kill(pid, timeout=args.timeout, verbose=args.verbose):
                    print("killed", pid, name, "on", port)
                    out.append({"port": port, "pid": pid, "name": name, "status": "killed"})
            else:
                print("skipped", pid)
                out.append({"port": port, "pid": pid, "name": name, "status": "skipped"})

    if args.json and out:
        print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
