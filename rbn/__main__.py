from . import listen_forever, band_mapping
import argparse
import sys
from .models import Callsign, Spot
from expiringdict import ExpiringDict
import curses

# Load rich console
from rich.logging import RichHandler
import logging

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)


def main(stdscr) -> int:

    ap = argparse.ArgumentParser(
        prog="rbn", description="CLI frontend to the Reverse Beacon Network"
    )
    ap.add_argument("-c", "--callsign", help="Your callsign", type=str, required=True)
    ap.add_argument(
        "-b",
        "--band",
        action="append",
        help="Band to filter by (this can be passed multiple times)",
        choices=[
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
            "2m",
        ],
    )
    ap.add_argument(
        "-m",
        "--mode",
        action="append",
        help="Mode to filter by (this can be passed multiple times)",
        choices=["cw", "rtty", "psk31", "psk63", "ft8", "ft4"],
    )
    ap.add_argument(
        "-f",
        "--filter-call",
        action="append",
        help="Callign to filter by (this can be passed multiple times)",
    )
    args = ap.parse_args()

    spot_queue = ExpiringDict(max_len=4096, max_age_seconds=60 * 15)

    # Build callback method
    async def callback(spot: Spot):

        # Filter out any unwanted modes
        if args.mode:
            if spot.mode.lower() not in args.mode:
                return

        # Filter out any unwanted callsigns
        if args.filter_call:
            for call in args.filter_call:
                call: str = call.upper()

                if call == spot.spotter.upper() or call == spot.spotted.upper():
                    break
            else:
                return

        # Filter out any unwanted bands
        if args.band:
            if (
                spot.frequency < band_mapping[args.band][0]
                or spot.frequency > band_mapping[args.band][1]
            ):
                return

        if not (spot.spotter.hasprefix("VE6") or spot.spotted.hasprefix("VE6")):
            return

        spot_queue[spot.spotted] = spot
        # Print the spot

    # Begin loop
    listen_forever(args.callsign, callback, spot_queue, stdscr)


if __name__ == "__main__":

    sys.exit(curses.wrapper(main))
