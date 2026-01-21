import threading
import time
import sys

counter = 0
ITERATIONS = 100_000

class IncrementThread(threading.Thread):
    def run(self):
        global counter
        for _ in range(ITERATIONS):
            # Эти три операции НЕ атомарны - состояние гонки неизбежно
            local = counter
            local += 1
            counter = local

class DecrementThread(threading.Thread):
    def run(self):
        global counter
        for _ in range(ITERATIONS):
            local = counter
            local -= 1
            counter = local

def main(n, m):
    global counter
    counter = 0
    threads = []

    start_time = time.time()

    # Создаем и запускаем потоки увеличения
    for _ in range(n):
        t = IncrementThread()
        threads.append(t)
        t.start()

    # Создаем и запускаем потоки уменьшения
    for _ in range(m):
        t = DecrementThread()
        threads.append(t)
        t.start()

    # Ожидаем завершения всех потоков
    for t in threads:
        t.join()

    end_time = time.time()

    expected = (n - m) * ITERATIONS
    print(f"Expected counter value: {expected}")
    print(f"Actual counter value: {counter}")
    print(f"Time elapsed: {end_time - start_time:.4f} seconds")
    print(f"Difference: {counter - expected}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Test3.py <num_increment_threads> <num_decrement_threads>")
        sys.exit(1)
    
    try:
        n = int(sys.argv[1])
        m = int(sys.argv[2])
        if n <= 0 or m <= 0:
            raise ValueError("Thread counts must be positive integers")
        main(n, m)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)