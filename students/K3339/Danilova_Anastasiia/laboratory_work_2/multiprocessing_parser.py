from multiprocessing import Process
import time

from parser_utils import parse_page
from urls import URLS


def main():
    processes = []

    start = time.time()

    for url in URLS:
        process = Process(target=parse_page, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end = time.time()
    print(f"Multiprocessing time: {end - start}")


if __name__ == "__main__":
    main()