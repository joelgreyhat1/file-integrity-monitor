import argparse
import time
from monitor.scanner import scan_directory
from monitor.baseline import save_baseline, load_baseline
from monitor.comparator import compare, print_alerts

def main():
    parser = argparse.ArgumentParser(description="File integrity monitor — watches a directory for unauthorized changes.")
    parser.add_argument("directory", help="Directory to monitor")
    parser.add_argument("--interval", type=int, default=30, help="Seconds between scans (default: 30)")
    parser.add_argument("--baseline", action="store_true", help="Create a fresh baseline and exit")
    args = parser.parse_args()

    if args.baseline:
        print(f"Scanning {args.directory} to create baseline...")
        snapshot = scan_directory(args.directory)
        save_baseline(snapshot)
        return

    baseline = load_baseline()
    if not baseline:
        print("No baseline found. Run with --baseline first to create one.")
        return

    print(f"Monitoring {args.directory} every {args.interval}s...")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            current = scan_directory(args.directory)
            alerts = compare(baseline, current)
            print_alerts(alerts)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()