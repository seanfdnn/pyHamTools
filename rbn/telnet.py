import asyncio
from .logging import RBN_LOGGER

# Telnet addresses:
# telnet.reversebeacon.net:7000 (CW, RTTY, ...)
# telnet.reversebeacon.net:7001 (FT8, FT4, ...)

def do_login(reader, writer, username: str) -> None:
    
    while True:
        
        # Read stream
        stream = yield from reader.read(1024)
        
        # If no stream, no data
        if not stream: 
            RBN_LOGGER.debug("Broken stream during login")
            return
        
        # Check for login prompt
        if "Please enter your call:" in stream:
            RBN_LOGGER.debug(f"Logging in as: {username}")
            writer.write(f"{username}\r\n")
            return

@asyncio.coroutine
def cw_telnet_handler(reader, writer, username: str, callback) -> None:
    
    # Handle login
    do_login(reader, writer, username)
    RBN_LOGGER.debug("Logged in")
    
    # Handle data
    while True:
        
        # Read stream
        stream = yield from reader.read(1024)
        
        # If no stream, no data
        if not stream: 
            RBN_LOGGER.debug("Broken stream during loop")
            return
        
        print(stream)
        

@asyncio.coroutine
def ft8_telnet_handler(reader, writer, username: str, callback) -> None:
    
    # Handle login
    do_login(reader, writer, username)
    RBN_LOGGER.debug("Logged in")
    
    # Handle data
    while True:
        
        # Read stream
        stream = yield from reader.read(1024)
        
        # If no stream, no data
        if not stream: 
            RBN_LOGGER.debug("Broken stream during loop")
            return
        
        