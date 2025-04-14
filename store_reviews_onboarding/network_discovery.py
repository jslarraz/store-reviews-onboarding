import psutil
import subprocess
import threading


def list_interfaces():
    interfaces = psutil.net_if_addrs()
    for key, val in interfaces.items():
        print(key, val[0].address)


def ping(dest_address, reachable_addresses):
    p = subprocess.run(["ping", dest_address, "-c", "2"], capture_output=True)
    if p.returncode == 0:
        reachable_addresses.append(dest_address)


def scan_network(interface):
    interfaces = psutil.net_if_addrs()
    if interface not in interfaces:
        print(f"Interface {interface} not found.")
        list_interfaces()
        exit(-1)

    threads = []
    reachable_addresses = []
    base_address = interfaces[interface][0].address
    base_address = base_address.split(".")
    for i in range(1, 255):
        base_address[3] = str(i)
        dest_address = ".".join(base_address)

        thread = threading.Thread(target=ping, args=(dest_address, reachable_addresses))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return reachable_addresses


def main():
    import argparse
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="command", help="Command to perform.", required=True
    )

    list_subparser = subparsers.add_parser(
        'list', help='List available network interfaces.'
    )

    scan_subparser = subparsers.add_parser(
        'scan', help='Scan the network for the given network interface.'
    )
    scan_subparser.add_argument(
        'interface', help='Network interface to scan.'
    )

    args = parser.parse_args()

    if args.command == 'list':
        list_interfaces()
    elif args.command == 'scan':
        reachable_addresses = scan_network(args.interface)
        print(reachable_addresses)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
