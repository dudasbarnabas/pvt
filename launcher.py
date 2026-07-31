import subprocess
import sys

from pvt_exp import main as run_experiment
from version_cont import main as version

from send_data import env_check as env_check


def start_experiment() -> None:
    print("\nStarting experiment...\n")

    if getattr(sys, "frozen", False):
        # Inside the PyInstaller executable, start another instance
        # of the same executable in experiment mode.
        command = [sys.executable, "--run-experiment"]
    else:
        # While testing directly with Python.
        command = [sys.executable, __file__, "--run-experiment"]

    result = subprocess.run(command, check=False)

    print(f"\nExperiment finished with exit code {result.returncode}.\n")


def launcher() -> None:
    print("=" * 45)
    print("PsychoPy Experiment Launcher")
    print("=" * 45)

    while True:
        command = input("\nCommand [start / exit]: ").strip().lower()

        if command == "start":
            start_experiment()

        elif command in {"exit", "quit", "q"}:
            print("Closing launcher.")
            break

        elif command == "":
            continue

        else:
            print(f"Unknown command: {command}")


def main() -> None:
    if "--run-experiment" in sys.argv:
        run_experiment()
    else:
        version()
        env_check()
        launcher()


if __name__ == "__main__":
    main()