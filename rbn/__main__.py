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


def is_freq_in_one_of_bands(freq, bands) -> bool:
    if not bands:
        return True
    for band in bands:
        if freq > band_mapping[band][0] and freq < band_mapping[band][1]:
            return True
    return False


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
        help="Callsign to filter by (this can be passed multiple times)",
    )

    ap.add_argument("-m", "--min-snr", help="Minimum SNR in dB", type=int)

    ap.add_argument("-w", "--max-wpm", help="Maximum Words per Minute", type=int)

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
                if call == spot.spotter or call == spot.spotted:
                    break
            else:
                return

        if not is_freq_in_one_of_bands(spot.frequency, args.band):
            return

        spot_queue[spot.spotted] = spot
        # Print the spot

    # Begin loop
    listen_forever(args.callsign, callback, spot_queue, stdscr)


def parse_dxcc():
    from . import dxcc_parser


if __name__ == "__main__":
    # parse_dxcc()

    sys.exit(curses.wrapper(main))
