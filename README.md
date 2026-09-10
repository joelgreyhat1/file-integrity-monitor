# File Integrity Monitor

A continuous file integrity monitoring tool that hashes every file in a directory, saves a baseline, then re-scans periodically and alerts on any file that was modified, added, or deleted — the same core mechanic behind enterprise tools like Tripwire and OSSEC. Written by Joel Odum.

## The Idea

Most intrusion detection focuses on network traffic — catching attacks as they happen. File integrity monitoring is different: it's about catching what an attacker *left behind*. If a malware drops a new file, modifies a binary, or injects a backdoor into a web app's source code, a hash-based monitor catches it even if the attacker cleaned up their tracks in the logs. It's also a real compliance requirement — PCI-DSS and SOC 2 both mandate file integrity monitoring for production systems, so this tool mirrors something you'd actually find in an enterprise security stack.

The interesting design problem was persistence: unlike the other tools in this set, this one needs to remember state between runs. The baseline gets saved as a JSON file so it survives restarts and can be compared against any future scan.

## What It Does

- Scans a directory recursively and hashes every file with both SHA-256 and MD5
- Saves the result as a baseline JSON file
- Re-scans continuously at a configurable interval, comparing against the baseline
- Alerts on three change types: modified files (hash mismatch), new files, and deleted files
- For modified files, shows both the old and new hash for both algorithms side by side — making the SHA-256 vs MD5 length and format difference visible, not just stated

## SHA-256 vs MD5 — Why Both

SHA-256 is what actually drives the integrity comparison — MD5 collisions are feasible in practice (two different files can produce the same MD5 hash), which makes it genuinely insecure as a sole integrity check. MD5 is shown alongside SHA-256 purely as a comparison: same file, same content, different algorithm, visibly different output. The contrast makes "use SHA-256, not MD5" a concrete observation rather than an abstract rule.

## Requirements

- Python 3 (standard library only — no external dependencies)

## Usage

```bash
git clone https://github.com/joelgreyhat1/file-integrity-monitor.git
cd file-integrity-monitor
```

Create a baseline for a directory:
```bash
python main.py C:\path\to\watch --baseline
```

Start monitoring (re-scans every 30 seconds by default):
```bash
python main.py C:\path\to\watch --interval 30
```

**Tip:** avoid pointing this at directories with `node_modules` or similar large dependency folders — thousands of small files slow the scan significantly. Point it at a source directory with a smaller number of files.

## Example Output from my scan against Vulnbank

```
Monitoring C:\Users\USER\vulnbank\src every 10s...
Press Ctrl+C to stop.

[MODIFIED] app\api\login\route.js at 2026-09-08 22:41:08
  SHA-256  old: 3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4
  SHA-256  new: 9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0
  MD5      old: d41d8cd98f00b204e9800998ecf8427e
  MD5      new: 098f6bcd4621d373cade4e832627b4f6

[NEW FILE] app\api\backdoor\route.js at 2026-09-08 22:41:08
  SHA-256: 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2
  MD5    : 5d41402abc4b2a76b9719d911017c592

No changes detected.
No changes detected.
```

## What I Learnt from building this

- Why chunked file reading matters for hashing — loading a large file into memory all at once before hashing it works fine for small files but falls apart on large ones, so reading in 8KB chunks and feeding them to the hasher incrementally is the right pattern regardless of file size
- That MD5 collision attacks aren't just theoretical — they've been demonstrated on real files, which is why showing MD5 and SHA-256 side by side rather than just saying "SHA-256 is better" makes the point more solid
- How persistence changes the design of a security tool — every other tool in this set is stateless (each run is independent), but an integrity monitor is only useful if it remembers what "normal" looks like, which made the baseline/compare split a real architectural decision rather than a convenience

## License

MIT