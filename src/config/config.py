import os
import socket
from dotenv import load_dotenv


load_dotenv()
HOST = os.getenv("HOST", None)
PORT = os.getenv("PORT", "80")

import os
import socket
from dotenv import load_dotenv

load_dotenv()

# Clean env parsing
HOST = os.getenv("HOST") or None
PORT = int(os.getenv("PORT", 8000))

FAMILY_MAP = {
    "AF_INET": socket.AF_INET,
    "AF_INET6": socket.AF_INET6,
}

TYPE_MAP = {
    "SOCK_STREAM": socket.SOCK_STREAM,
    "SOCK_DGRAM": socket.SOCK_DGRAM,
}

FAMILY = FAMILY_MAP.get(os.getenv("FAMILY", "AF_INET"))
TYPE = TYPE_MAP.get(os.getenv("TYPE", "SOCK_STREAM"))
