"""Compare two systems and guard against deleting too much."""

def compare(src, tgt):
    """src and tgt map record id -> checksum. Returns the differences."""
    missing = sorted(set(src) - set(tgt))
    orphans = sorted(set(tgt) - set(src))
    changed = sorted(k for k in set(src) & set(tgt) if src[k] != tgt[k])
    return {"count_src": len(src), "count_tgt": len(tgt),
            "missing_in_target": missing, "orphans_in_target": orphans,
            "changed": changed}

def deletion_guard(report, max_fraction=0.05):
    """Return the ids that may be deleted, or refuse if there are too many."""
    n = len(report["orphans_in_target"])
    total = report["count_tgt"]
    if total and n / total > max_fraction:
        raise RuntimeError("refusing to delete %d of %d records" % (n, total))
    return report["orphans_in_target"]
