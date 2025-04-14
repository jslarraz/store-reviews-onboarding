import tkinter as tk
from tkinter import ttk

import threading
import requests
from store_reviews_onboarding.network_discovery import scan_network


def request(dest_addr, stats):
    stats[dest_addr] = {"cpu_percent": "-", "memory_usage": "-"}
    try:
        r = requests.get(f"http://{dest_addr}:{8080}", timeout=10)
        if r.status_code == 200:
            stats[dest_addr] = r.json()
    except:
        pass

def get_stats(reachable_addresses):
    threads = []
    stats = {}
    for dest_address in reachable_addresses:
        thread = threading.Thread(target=request, args=(dest_address, stats))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return stats


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("interface", type=str, help="Network interface to monitor.")
    args = parser.parse_args()

    root = tk.Tk()

    # Add header
    header = ttk.Frame(root)
    header.pack(fill=tk.BOTH, side=tk.TOP)

    IP = tk.Label(header, width=20, text="IP address")
    IP.pack(side=tk.LEFT)
    CPU = tk.Label(header, width=20, text="cpu_percent")
    CPU.pack(side=tk.RIGHT)
    MEM = tk.Label(header, width=20, text="memory_usage")
    MEM.pack(side=tk.RIGHT)

    # Fill the table
    reachable_addresses = scan_network(args.interface)
    stats = get_stats(reachable_addresses)
    for address in stats:
        row = ttk.Frame(root)
        row.pack(fill=tk.BOTH, side=tk.TOP)

        IP = tk.Label(row, width=20,  text=address)
        IP.pack(side=tk.LEFT)
        CPU = tk.Label(row, width=20, text=f"{stats[address]['cpu_percent']} %")
        CPU.pack(side=tk.RIGHT)
        MEM = tk.Label(row, width=20, text=f"{stats[address]['memory_usage']} %")
        MEM.pack(side=tk.RIGHT)

    tk.mainloop()


if __name__ == "__main__":
    main()
