"""Process records one by one: quarantine bad data, fail loudly on the rest."""
import json, logging, uuid

log = logging.getLogger("sync")

def process(records, upsert, quarantine_path, run_id=None):
    """Returns run counts. ValueError means bad data: park it and go on.
    Any other exception (network, bug) stops the run: do not hide it."""
    run_id = run_id or uuid.uuid4().hex[:8]
    counts = {"run_id": run_id, "read": 0, "written": 0, "quarantined": 0}
    with open(quarantine_path, "a") as parked:
        for rec in records:
            counts["read"] += 1
            try:
                upsert(rec)
                counts["written"] += 1
            except ValueError as err:
                counts["quarantined"] += 1
                parked.write(json.dumps({"run_id": run_id, "reason": str(err),
                                         "record": rec}) + "\n")
                log.warning("quarantined id=%s run=%s reason=%s",
                            rec.get("id"), run_id, err)
    log.info("run summary %s", json.dumps(counts))
    return counts
