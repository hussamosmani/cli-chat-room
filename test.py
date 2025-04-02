import sys
import threading
import time
import readchar

input_buffer = ""


def func():
    time.sleep(5)
    sys.stdout.write("\r\033[K")
    # sys.stdout.flush()
    message = "bob: hi"
    sys.stdout.write(f"----{message}----\n")
    sys.stdout.write(f"{input_buffer}")
    sys.stdout.flush()


t = threading.Thread(target=func)
t.start()

while True:
    key = readchar.readkey()
    if key in ("\x08", "\x7f"):
        input_buffer[:-1]
        sys.stdout.write("\b \b")
        sys.stdout.flush()
    else:
        input_buffer += key
        sys.stdout.write(key)
        sys.stdout.flush()
