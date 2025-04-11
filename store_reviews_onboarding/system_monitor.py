import psutil


def stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory()
    return cpu_percent, memory_usage.percent


def main():
    cpu_percent, memory_usage = stats()
    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory Usage: {memory_usage}%")


if __name__ == "__main__":
    main()
