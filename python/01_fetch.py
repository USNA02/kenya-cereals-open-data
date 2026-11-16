"""Fetch the launch dataset. Save raw files. Do not edit them later."""
from pathlib import Path
import subprocess
import urllib.error
import urllib.request

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

FILES = {
    "cereal_yield.csv": "https://ourworldindata.org/grapher/cereal-yield.csv",
    "cereal_production.csv": "https://ourworldindata.org/grapher/cereal-production.csv",
    "ag_employment.csv": "https://ourworldindata.org/grapher/share-of-the-labor-force-employed-in-agriculture.csv",
    "ag_land.csv": "https://ourworldindata.org/grapher/agricultural-land.csv",
    "cereal_area.csv": "https://datahub.io/world-development-indicators/ag.lnd.crel.ha/_r/-/data.csv",
    "ag_gdp.csv": "https://datahub.io/world-development-indicators/nv.agr.totl.zs/_r/-/data.csv",
    "fertilizer.csv": "https://datahub.io/world-development-indicators/ag.con.fert.zs/_r/-/data.csv",
    "rural.csv": "https://datahub.io/world-development-indicators/sp.rur.totl.zs/_r/-/data.csv",
    "ag_land_pct.csv": "https://datahub.io/world-development-indicators/ag.lnd.agri.zs/_r/-/data.csv",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": "text/csv,text/plain,*/*",
}


def download(url, dest):
    request = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            dest.write_bytes(response.read())
        return
    except urllib.error.HTTPError as err:
        if err.code != 403:
            raise
        print("  Python was refused; retrying with curl")
    subprocess.run(
        ["curl.exe", "-fsSL", "-A", HEADERS["User-Agent"], "-o", str(dest), url],
        check=True,
    )


for name, url in FILES.items():
    dest = RAW / name
    print(f"downloading {name}")
    download(url, dest)
    print(f"{name}: {dest.stat().st_size:,} bytes")