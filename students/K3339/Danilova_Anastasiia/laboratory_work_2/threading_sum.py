import threading
import time

TOTAL = 100_000_000
THREADS_COUNT = 4

results = [0] * THREADS_COUNT


def calculate_sum(start, end, index):
    total = 0

    for i in range(start, end + 1):
        total += i

    results[index] = total


def main():
    threads = []

    chunk_size = TOTAL // THREADS_COUNT

    start_time = time.time()

    for i in range(THREADS_COUNT):
        start_num = i * chunk_size + 1

        if i == THREADS_COUNT - 1:
            end_num = TOTAL
        else:
            end_num = (i + 1) * chunk_size

        thread = threading.Thread(
            target=calculate_sum,
            args=(start_num, end_num, i)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    final_sum = sum(results)

    end_time = time.time()

    print(f"Sum: {final_sum}")
    print(f"Time: {end_time - start_time:.2f} sec")


if __name__ == "__main__":
    main()
