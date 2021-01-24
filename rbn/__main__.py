import argparse
import sys

# Load rich console
from rich.traceback import install
from rich.logging import RichHandler
import logging
install()
logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

from . import listen_forever

def main() -> int:

    ap = argparse.ArgumentParser(
        prog="rbn", description="CLI frontend to the Reverse Beacon Network")
    ap.add_argument("-c", "--callsign", help="Your callsign", type=str, required=True)
    ap.add_argument("-b", "--bands", action="append", help="Band to filter by (this can be passed multiple times)", choices=[
        "630m",
        "160m",
        "80m",
        "60m",
        "40m",
        "30m",
        "20m",
        "17m",
        "15m",
        "12m",
        "10m",
        "6m",
        "4m",
        "2m"
    ])
    ap.add_argument("-m", "--mode", action="append", help="Mode to filter by (this can be passed multiple times)", choices=[
        "cw", "rtty", "psk31", "psk63", "ft8", "ft4"
    ])
    args = ap.parse_args()
    
    # Build callback method
    def callback(spotter: str, spotted: str, frequency: float, mode: str, snr: int, message: str, time: str):
        print(f"{spotter} -> {spotted}")
        
    # Begin loop
    listen_forever(args.callsign, callback)


if __name__ == "__main__":
    sys.exit(main())
