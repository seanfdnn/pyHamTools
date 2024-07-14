import qrzlib
import os
from dataclasses import dataclass

QRZ_USERNAME = os.environ.get("QRZ_USERNAME")
QRZ_PASSWORD = os.environ.get("QRZ_PASSWORD")

if not QRZ_USERNAME:
    print("Environment variable QRZ_USERNAME must be set")
    exit(1)

if not QRZ_PASSWORD:
    print("Environment variable QRZ_PASSWORD must be set")
    exit(1)

qrz = qrzlib.QRZ()
qrz.authenticate(QRZ_USERNAME, QRZ_PASSWORD)


@dataclass
class CallsignHolder:
    fullname: str
    grid: str
    country: str
    state: str
    email: str


def get_call(callsign: str) -> CallsignHolder:
    try:
        qrz.get_call(callsign)
        return CallsignHolder(qrz.fullname, qrz.grid, qrz.country, qrz.state, qrz.email)
    except:
        return None
