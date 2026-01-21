import threading
import time
import sys

counter = 0
lock = threading.RLock()  # Рекурсивная блокировка
ITERATIONS = 100_000

class IncrementThread(threading.Thread):
    def run(self):
        global counter
        for _ in range(ITERATIONS):
            with lock:  # RLock позволяет перезахватывать из того же потока
                counter += 1

class DecrementThread(threading.Thread):
    def run(self):
        global counter
        for _ in range(ITERATIONS):
            with lock:
                counter -= 1

def main(n, m):
    global counter
    counter = 0
    threads = []

    start_time = time.time()

    # Создаем и запускаем потоки
    for _ in range(n):
        t = IncrementThread()
        threads.append(t)
        t.start()

    for _ in range(m):
        t = DecrementThread()
        threads.append(t)
        t.start()

    # Ожидаем завершения
    for t in threads:
        t.join()

    end_time = time.time()

    expected = (n - m) * ITERATIONS
    print(f"Expected counter value: {expected}")
    print(f"Actual counter value: {counter}")
    print(f"Time elapsed: {end_time - start_time:.4f} seconds")
    print(f"Correct: {counter == expected}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Test3C.py <num_increment_threads> <num_decrement_threads>")
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