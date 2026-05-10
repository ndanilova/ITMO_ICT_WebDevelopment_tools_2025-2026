import threading
import time

from parser_utils import parse_page
from urls import URLS


threads = []

start = time.time()

for url in URLS:
    thread = threading.Thread(target=parse_page, args=(url,))
    threads.append(thread)

    thread.start()


for thread in threads:
    thread.join()


end = time.time()

print(f"Threading time: {end - start}")