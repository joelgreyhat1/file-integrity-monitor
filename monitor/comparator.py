from datetime import datetime

def compare(baseline, current):
    alerts = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # files that existed in the baseline but are now gone :()
    for filepath in baseline:
        if filepath not in current:
            alerts.append({
                "type": "DELETED",
                "file": filepath,
                "time": now,
            })

    # new files that weren't in the baseline :)
    for filepath in current:
        if filepath not in baseline:
            alerts.append({
                "type": "NEW FILE",
                "file": filepath,
                "time": now,
                "sha256": current[filepath]["sha256"],
                "md5": current[filepath]["md5"],
            })

    # files that exist in both but whose hashes changed
    for filepath in baseline:
        if filepath in current:
            if current[filepath]["sha256"] != baseline[filepath]["sha256"]:
                alerts.append({
                    "type": "MODIFIED",
                    "file": filepath,
                    "time": now,
                    "old_sha256": baseline[filepath]["sha256"],
                    "new_sha256": current[filepath]["sha256"],
                    "old_md5": baseline[filepath]["md5"],
                    "new_md5": current[filepath]["md5"],
                })

    return alerts


def print_alerts(alerts):
    if not alerts:
        print("No changes detected.")
        return

    for alert in alerts:
        print(f"\n[{alert['type']}] {alert['file']} at {alert['time']}")
        if alert["type"] == "MODIFIED":
            print(f"  SHA-256  old: {alert['old_sha256']}")
            print(f"  SHA-256  new: {alert['new_sha256']}")
            print(f"  MD5      old: {alert['old_md5']}")
            print(f"  MD5      new: {alert['new_md5']}")
        elif alert["type"] == "NEW FILE":
            print(f"  SHA-256: {alert['sha256']}")
            print(f"  MD5    : {alert['md5']}")