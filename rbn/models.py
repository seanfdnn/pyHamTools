from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import timeago
from . import dxcc_parser
from . import qrz


# Print iterations progress
def printProgressBar(
    iteration, total, prefix="", suffix="", decimals=1, length=100, fill="█"
):
    """
    Call in a loop to create terminal progress bar
    @params:
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    filledLength = int(length * min(iteration, total) // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    value_str = f"({iteration} dB)".ljust(7)
    return f"\r{prefix} |{bar}| {value_str}"


class Callsign:
    """Represents an amateur radio callsign"""

    def __init__(self, callsign: str) -> None:

        # Canonicalize
        self.callsign_str = callsign.upper().strip()
        self.owner = None
        self._dx_entity = None

    def __hash__(self) -> int:
        return hash(self.callsign_str)

    def __eq__(self, value: object) -> bool:
        return value.callsign_str == self.callsign_str

    def __repr__(self) -> str:
        return self.callsign_str

    def hasprefix(self, prefix: str) -> bool:
        return self.callsign_str.startswith(prefix.upper())

    def get_dxcc_entity(self) -> dxcc_parser.DXCCEntity:
        if self._dx_entity is None:
            self._dx_entity = dxcc_parser.dxcc_entities.get_entity_for_callsign(
                self.callsign_str
            )

    @property
    def country_code(self) -> str:
        self.get_dxcc_entity()
        return self._dx_entity.country_code if self._dx_entity else "??"

    async def resolve_owner(self):
        pass
        # self.owner = qrz.get_call(self.callsign_str)

    @property
    def owner_name(self):
        if not self.owner:
            self.resolve_owner()
        return self.owner.fullname if self.owner else ""


@dataclass
class Spot:
    spotter: Callsign
    spotted: Callsign
    frequency: float
    mode: str
    strength: int
    time: datetime

    def age(self) -> timedelta:
        return datetime.now(timezone.utc) - self.time

    def __str__(self):
        return f"{printProgressBar(self.strength, total=30, length=15)} {str(self.spotted).ljust(8)} {self.spotted.country_code} {timeago.format(self.time, datetime.now(timezone.utc)).ljust(14)} on {self.frequency} {self.spotted.owner_name} "
