"""Incremental sync: watermark, overlap window, atomic checkpoints."""
import json, os, tempfile
from datetime import datetime, timedelta, timezone
from client import iter_records

FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

def load_watermark(path, default="1970-01-01T00:00:00.000000Z"):
    try:
        with open(path) as f:
            return json.load(f)["watermark"]
    except FileNotFoundError:
        return default

def save_watermark(path, value):
    """Write to a temp file, then rename: a crash can never leave half a file."""
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(path)))
    with os.fdopen(fd, "w") as f:
        json.dump({"watermark": value}, f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)

def run_once(session, base_url, state_path, upsert, overlap_seconds=120):
    """Fetch records changed since the last watermark (minus an overlap) and
    upsert them. Returns the number of records processed."""
    wm = load_watermark(state_path)
    start = datetime.strptime(wm, FMT).replace(tzinfo=timezone.utc)
    since = (start - timedelta(seconds=overlap_seconds)).strftime(FMT)
    newest, count = wm, 0
    url = base_url + "/orders"
    for rec in iter_records(session, url, {"updatedSince": since}):
        upsert(rec)               # must be idempotent: overlap repeats rows
        newest = max(newest, rec["updatedAt"])
        count += 1
    save_watermark(state_path, newest)   # commit only after the batch succeeded
    return count
