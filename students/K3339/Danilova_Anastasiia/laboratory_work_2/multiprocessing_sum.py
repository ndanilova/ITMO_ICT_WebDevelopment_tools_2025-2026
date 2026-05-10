import multiprocessing
import time

TOTAL = 100_000_000
PROCESSES_COUNT = 10



def calculate_sum(start, end, queue):
    total = 0

    for i in range(start, end + 1):
        total += i

    queue.put(total)


def main():
    processes = []

    queue = multiprocessing.Queue()

    chunk_size = TOTAL // PROCESSES_COUNT

    start_time = time.time()

    for i in range(PROCESSES_COUNT):

        start_num = i * chunk_size + 1

        if i == PROCESSES_COUNT - 1:
            end_num = TOTAL
        else:
            end_num = (i + 1) * chunk_size

        process = multiprocessing.Process(
            target=calculate_sum,
            args=(start_num, end_num, queue)
        )

        processes.append(process)

        process.start()

    for process in processes:
        process.join()

    results = []

    while not queue.empty():
        results.append(queue.get())

    final_sum = sum(results)

    end_time = time.time()

    print(f"Sum: {final_sum}")
    print(f"Time: {end_time - start_time:.2f} sec")


if __name__ == "__main__":
    main()
