import asyncio
import time

TOTAL = 100_000_000
TASKS_COUNT = 4


async def calculate_sum(start, end):
    total = 0

    for i in range(start, end + 1):
        total += i

    return total


async def main():
    tasks = []

    chunk_size = TOTAL // TASKS_COUNT

    start_time = time.time()

    for i in range(TASKS_COUNT):

        start_num = i * chunk_size + 1

        if i == TASKS_COUNT - 1:
            end_num = TOTAL
        else:
            end_num = (i + 1) * chunk_size

        task = asyncio.create_task(
            calculate_sum(start_num, end_num)
        )

        tasks.append(task)

    results = await asyncio.gather(*tasks)

    final_sum = sum(results)

    end_time = time.time()

    print(f"Sum: {final_sum}")
    print(f"Time: {end_time - start_time:.2f} sec")


if __name__ == "__main__":
    asyncio.run(main())
