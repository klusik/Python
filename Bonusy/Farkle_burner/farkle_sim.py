import random
import multiprocessing as mp
import threading
import sys
import time
import queue
import json


# === FARKLE GAME LOGIC ===

def roll_dice(num_dice=6):
    return [random.randint(1, 6) for _ in range(num_dice)]


def score_dice(dice):
    score = 0
    counts = {i: dice.count(i) for i in range(1, 7)}
    for n in range(1, 7):
        if counts[n] >= 3:
            if n == 1:
                score += 1000 * (2 ** (counts[n] - 3))
            else:
                score += n * 100 * (2 ** (counts[n] - 3))
            counts[n] -= 3
    score += counts[1] * 100
    score += counts[5] * 50
    return score


def simple_farkle_strategy():
    dice = roll_dice(6)
    score = score_dice(dice)
    return score


def farkle_worker(worker_id, result_queue, stop_event, config):
    random.seed()
    games_played = 0
    total_score = 0
    highest_score = 0
    scores = []

    num_games = config.get('games_per_worker', 100000)

    while not stop_event.is_set() and games_played < num_games:
        score = simple_farkle_strategy()
        scores.append(score)
        total_score += score
        games_played += 1
        if score > highest_score:
            highest_score = score
        if games_played % 1000 == 0:
            result_queue.put({
                'worker_id': worker_id,
                'type': 'progress',
                'games_played': games_played,
                'avg_score': total_score / games_played,
                'highest_score': highest_score
            })
    # Final result
    avg_score = total_score / games_played if games_played else 0
    result_queue.put({
        'worker_id': worker_id,
        'type': 'final',
        'games_played': games_played,
        'avg_score': avg_score,
        'highest_score': highest_score,
        'scores': scores[:10000]
    })


def keyboard_listener(stop_event):
    print("\nPress SPACE to stop the simulation early...")
    try:
        import msvcrt
        while not stop_event.is_set():
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b' ':
                    stop_event.set()
                    break
            time.sleep(0.1)
    except ImportError:
        import select
        print(" (Click terminal and press SPACE) ")
        while not stop_event.is_set():
            if select.select([sys.stdin], [], [], 0.1)[0]:
                key = sys.stdin.read(1)
                if key == " ":
                    stop_event.set()
                    break


def ask_int(prompt, default):
    while True:
        inp = input(f"{prompt} [{default}]: ").strip()
        if not inp:
            return default
        try:
            val = int(inp)
            if val > 0:
                return val
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    print("=== Farkle Simulation ===")
    num_workers = ask_int("Enter number of worker processes", 4)
    games_per_worker = ask_int("Enter number of games per worker", 100000)

    config = {'games_per_worker': games_per_worker}
    mp.set_start_method('spawn', force=True)

    manager = mp.Manager()
    result_queue = manager.Queue()
    stop_event = manager.Event()
    worker_processes = []

    listener_thread = threading.Thread(target=keyboard_listener, args=(stop_event,), daemon=True)
    listener_thread.start()

    print(f"\nStarting {num_workers} worker processes, each will play up to {games_per_worker} games.")
    print("Simulation running. Press SPACE at any time to stop early.")
    for i in range(num_workers):
        p = mp.Process(target=farkle_worker, args=(i, result_queue, stop_event, config))
        p.start()
        worker_processes.append(p)

    all_results = []
    try:
        while not stop_event.is_set() or any(p.is_alive() for p in worker_processes):
            try:
                result = result_queue.get(timeout=0.5)
                if result['type'] == 'progress':
                    print(f"Worker {result['worker_id']} progress: "
                          f"{result['games_played']} games, "
                          f"avg score {result['avg_score']:.2f}, "
                          f"high score {result['highest_score']}")
                elif result['type'] == 'final':
                    all_results.append(result)
            except queue.Empty:
                continue
    except KeyboardInterrupt:
        print("\nStopping... please wait.")
        stop_event.set()

    print("Waiting for workers to finish...")
    for p in worker_processes:
        p.join()

    print("\nSimulation stopped. Results collected from workers:\n")
    for result in all_results:
        print(f"Worker {result['worker_id']}: "
              f"Games: {result['games_played']}, "
              f"Avg Score: {result['avg_score']:.2f}, "
              f"High Score: {result['highest_score']}")

    with open("farkle_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print("\nResults saved to farkle_results.json.")

    if all_results:
        best = max(all_results, key=lambda x: x['avg_score'])
        print(f"\nBest worker (by avg score): {best['worker_id']}, Avg Score: {best['avg_score']:.2f}")


if __name__ == "__main__":
    main()
