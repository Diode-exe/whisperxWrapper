import subprocess
import time

def main():
    time_to_run_non_turbo = time.perf_counter()
    print("Running whisperx.exe...")
    subprocess.run(["whisperx.exe", "--model", "large-v3", "--output_format", "all", "--language", "en", ".\\2026-04-26 10-37-35-shrunk.mp4"])
    time_to_run_non_turbo = time.perf_counter() - time_to_run_non_turbo
    print(f"Time taken: {time_to_run_non_turbo} seconds")

    time_to_run_turbo = time.perf_counter()
    print("Running whisperx.exe...")
    subprocess.run(["whisperx.exe", "--model", "large-v3-turbo", "--output_format", "all", "--language", "en", ".\\2026-04-26 10-37-35-shrunk.mp4"])
    time_to_run_turbo = time.perf_counter() - time_to_run_turbo
    print(f"Time taken: {time_to_run_turbo} seconds")

    print(f"Speedup: {time_to_run_non_turbo / time_to_run_turbo:.2f}x")
    print(f"{time_to_run_non_turbo:.2f} seconds (non-turbo) vs {time_to_run_turbo:.2f} seconds (turbo)")

if __name__ == "__main__":
    main()