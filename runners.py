"""Fetch today's and tomorrow's GB/IRE declared runners from the Racing Post API
and write runners_<date>.json. Runs in GitHub Actions (see .github/workflows/runners.yml).
Only public declarations are written here (horse, trainer, course, time, race) - no tour text."""
import json
import os
import glob
import urllib.request
from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
    UK = ZoneInfo("Europe/London")
except Exception:
    UK = timezone.utc

KEY = os.environ.get("RP_API_KEY", "").strip()
JWT = os.environ.get("RP_JWT_KEY", "").strip()
BASE = "https://api.rpb2b.io/horses/racecards"


def get(url):
    req = urllib.request.Request(url, headers={"x-api-key": KEY, "x-jwt-key": JWT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def off_time(s):
    try:
        dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        if dt.tzinfo:
            dt = dt.astimezone(UK)
        return dt.strftime("%H:%M")
    except Exception:
        return ""


def fetch_day(day):
    cards = get(f"{BASE}/date/{day}")
    lst = ((cards or {}).get("data") or {}).get("list") or {}
    meetings = lst.values() if isinstance(lst, dict) else lst
    runners, failed, races = [], 0, 0
    for m in meetings:
        if str(m.get("country_code")) not in ("GB", "IRE"):
            continue
        course = m.get("course_style_name") or m.get("course_name") or ""
        for race in m.get("races") or []:
            races += 1
            try:
                rr = get(f"{BASE}/runners/{race.get('race_instance_uid')}")
            except Exception:
                failed += 1
                continue
            rs = ((rr or {}).get("data") or {}).get("runners") or {}
            for run in (rs.values() if isinstance(rs, dict) else rs):
                runners.append({
                    "horse": str(run.get("horse_name") or ""),
                    "trainer": str(run.get("trainer_stylename") or ""),
                    "course": course,
                    "off": off_time(race.get("race_datetime")),
                    "race": str(race.get("race_instance_title") or ""),
                    "nonRunner": bool(run.get("non_runner")),
                })
    out = {"date": day, "fetched": datetime.now(timezone.utc).isoformat(), "failedRaces": failed, "runners": runners}
    with open(f"runners_{day}.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print(f"{day}: {len(runners)} runners in {races} races ({failed} failed)")


def main():
    if not KEY or not JWT:
        raise SystemExit("RP_API_KEY / RP_JWT_KEY secrets are missing")
    today = datetime.now(UK).date()
    keep = set()
    for i in (0, 1):
        day = (today + timedelta(days=i)).isoformat()
        keep.add(f"runners_{day}.json")
        try:
            fetch_day(day)
        except Exception as e:
            print(f"{day}: FAILED - {e}")
    for f in glob.glob("runners_*.json"):          # drop old days
        if os.path.basename(f) not in keep:
            os.remove(f)


if __name__ == "__main__":
    main()
