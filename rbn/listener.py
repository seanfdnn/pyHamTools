import asyncio
import telnetlib3
from .logging import RBN_LOGGER
from .telnet import telnet_handler
from typing import Callable
import curses
from datetime import datetime, timezone


async def print_screen(queue, stdscr):
    while True:
        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.move(0, 0)
        stdscr.addstr(datetime.now(timezone.utc).strftime("%H:%MZ %Y-%b-%d"))

        for idx, spot in enumerate(sorted(queue.values(), key=lambda x: x.age())):
            if idx < curses.LINES - 1:
                stdscr.move(idx + 1, 0)
                stdscr.addstr(str(spot))
        stdscr.refresh()
        await asyncio.sleep(1)


def listen_forever(
    callsign: str,
    callback: Callable[[str, str, float, str, int, str], None],
    queue,
    stdscr,
) -> asyncio.AbstractEventLoop:
    """Begin listening for events coming in from the Reverse Beacon Network

    Args:
        callsign (str): Your (or the user's) callsign
        callback (Callable[[spotter: str, spotted: str, frequency: float, mode: str, strength: int, timecode: str], None]): Callback function
    """

    # Get the event loop
    loop = asyncio.get_event_loop()

    # Coroutines for each Telnet server
    RBN_LOGGER.debug("Opening telnet connections")
    cw_coro = telnetlib3.open_connection(
        "telnet.reversebeacon.net",
        7000,
        shell=lambda r, w: telnet_handler(r, w, callsign, callback),
    )

    # Register with the event loop
    RBN_LOGGER.debug("Begining event loop")
    reader, writer = loop.run_until_complete(cw_coro)
    loop.run_until_complete(print_screen(queue, stdscr))
    loop.run_until_complete(writer.protocol.waiter_closed)

    return loop
