"""Watch for Lepro bulb joining TELUS5434 — check ARP + Tuya + ping sweep."""
import subprocess, socket, json, time

LEPRO_MAC = "70-89-76-25-fb-b3"
LOCAL_IP = "192.168.1.73"

print("=== WATCHING FOR LEPRO BULB (70:89:76:25:FB:B3) ===")
print("Continuous scan — ARP + Tuya broadcast + sweep")

cycle = 0
while True:
    cycle += 1
    
    # Check ARP
    arp = subprocess.run(["arp", "-a"], capture_output=True, text=True)
    for line in arp.stdout.splitlines():
        if "70-89-76" in line.lower():
            print(f"\n!!! LEPRO FOUND IN ARP: {line.strip()}")
            # Immediately probe Tuya ports
            ip = line.split()[0].strip()
            for port in [6668, 6666, 6667]:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                try:
                    s.connect((ip, port))
                    print(f"  TCP {port} OPEN on {ip}")
                    s.close()
                except:
                    s.close()
            # Try WiZ too
            us = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            us.settimeout(2)
            us.bind((LOCAL_IP, 0))
            try:
                us.sendto(json.dumps({"method":"getPilot","params":{}}).encode(), (ip, 38899))
                d, _ = us.recvfrom(4096)
                print(f"  WiZ response: {d.decode()}")
            except:
                pass
            us.close()
            print("DONE — Lepro located!")
            exit(0)
    
    # Quick broadcast for new ARP entries
    for i in range(60, 90):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.01)
            s.sendto(b"", (f"192.168.1.{i}", 1))
            s.close()
        except:
            pass
    
    if cycle % 5 == 0:
        print(f"[{time.strftime('%H:%M:%S')}] Cycle {cycle}... still watching")
    
    time.sleep(2)
