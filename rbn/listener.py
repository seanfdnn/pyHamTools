import asyncio
import telnetlib3
from .logging import RBN_LOGGER
from typing import Callable

from .telnet import telnet_handler, TelnetReaderUnicode, TelnetWriterUnicode


def listen_forever(callsign: str, callback: Callable[[str, str, float, str, int, str], None]) -> asyncio.AbstractEventLoop:
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
        'telnet.reversebeacon.net', 7000, shell=lambda r, w: telnet_handler(r, w, callsign, callback))
    ft8_coro = telnetlib3.open_connection(
        'telnet.reversebeacon.net', 7001, shell=lambda r, w: telnet_handler(r, w, callsign, callback))

    # Register with the event loop
    RBN_LOGGER.debug("Begining event loop")
    reader, writer = loop.run_until_complete(cw_coro)
    reader, writer = loop.run_until_complete(ft8_coro)
    loop.run_until_complete(writer.protocol.waiter_closed)

    return loop
