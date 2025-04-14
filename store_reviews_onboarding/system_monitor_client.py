import requests


def stats(host="localhost", port="8080"):
    r = requests.get(f"http://{host}:{port}")
    if r.status_code != 200:
        return None, None

    return r.json()["cpu_percent"], r.json()["memory_usage"]


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=int, help="Server addr.")
    parser.add_argument("--port", type=int, help="Server port.")
    args = parser.parse_args()

    host = args.host if args.host else "localhost"
    port = args.port if args.port else 8080

    cpu_percent, memory_usage = stats(host, port)
    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory Usage: {memory_usage}%")


if __name__ == "__main__":
    main()
