from . import listen_forever, band_mapping
import argparse
import sys

# Load rich console
from rich.logging import RichHandler
import logging
logging.basicConfig(
    level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)


def main() -> int:

    ap = argparse.ArgumentParser(
        prog="rbn", description="CLI frontend to the Reverse Beacon Network")
    ap.add_argument("-c", "--callsign", help="Your callsign",
                    type=str, required=True)
    ap.add_argument("-b", "--band", action="append", help="Band to filter by (this can be passed multiple times)", choices=[
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
    ap.add_argument("-f", "--filter-call", action="append",
                    help="Callign to filter by (this can be passed multiple times)")
    args = ap.parse_args()

    # Build callback method
    def callback(spotter: str, spotted: str, frequency: float, mode: str, strength: int, time: str):

        # Filter out any unwanted modes
        if args.mode:
            if mode.lower() not in args.mode:
                return

        # Filter out any unwanted callsigns
        if args.filter_call:
            for call in args.filter_call:
                call: str = call.upper()

                if call == spotter.upper() or call == spotted.upper():
                    break
            else:
                return

        # Filter out any unwanted bands
        if args.band:
            if frequency < band_mapping[args.band][0] or frequency > band_mapping[args.band][1]:
                return

        # Print the spot
        print(
            f"{spotter} spotted {spotted} on {frequency} using {mode} ({strength} dB) at {time}")

    # Begin loop
    listen_forever(args.callsign, callback)


if __name__ == "__main__":
    sys.exit(main())
