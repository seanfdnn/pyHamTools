import asyncio
from typing import List, Callable
import re
from telnetlib3.stream_reader import TelnetReaderUnicode
from telnetlib3.stream_writer import TelnetWriterUnicode

from .logging import RBN_LOGGER

# Telnet addresses:
# telnet.reversebeacon.net:7000 (CW, RTTY, ...)
# telnet.reversebeacon.net:7001 (FT8, FT4, ...

# REGEX rule that covers all data from RBN
BLANKET_EXPRESSION = r"^DX de ([A-Z\d\-\/]*)-#:\s+([\d.]*)\s+([A-Z\d\-\/]*)\s+([A-Z\d]*)\s+(\d*) dB.*\s+(\d{4}Z)"


@asyncio.coroutine
def telnet_handler(reader: TelnetReaderUnicode, writer: TelnetWriterUnicode, username: str, callback: Callable[[str, str, float, str, int, str], None]) -> None:
    """Handler function for every telnet packet the comes from RBN

    Args:
        reader (TelnetReaderUnicode): Stream reader
        writer (TelnetWriterUnicode): Stream writer
        username (str): Username of the calling user
        callback (Callable[[spotter: str, spotted: str, frequency: float, mode: str, strength: int, timecode: str], None]): Callback function
    """

    # Handle data
    while True:

        # Read stream
        stream = yield from reader.read(4096)

        # If no stream, no data
        if not stream:
            RBN_LOGGER.debug("Broken stream during loop")
            return

        # Check for login prompt
        if "Please enter your call:" in stream:
            RBN_LOGGER.debug(f"Logging in as: {username}")
            writer.write(f"{username}\r\n")
            continue

        # Get all data that came in this packet
        data = stream.split("\r\n")

        # Handle every entry
        for entry in data:

            # Skip empty data
            if not entry:
                continue

            # Sanitize data
            safe_data = entry.strip()

            # Extract data
            parsed: list[str] = re.findall(BLANKET_EXPRESSION, safe_data)

            if not parsed or len(parsed[0]) < 6:
                RBN_LOGGER.debug(f"Rejecting parsed data")
                continue

            spotter: str = parsed[0][0]
            frequency: float = float(parsed[0][1])
            spotted: str = parsed[0][2]
            mode: str = parsed[0][3]
            strength: int = int(parsed[0][4])
            time: str = parsed[0][5]

            # Call the callback
            if callback:
                RBN_LOGGER.debug(f"Calling callback")
                callback(spotter, spotted, frequency, mode, strength, time)
            else:
                RBN_LOGGER.debug(f"No callback to call")
