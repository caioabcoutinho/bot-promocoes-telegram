"""Start the Telegram monitor and command bot as one managed application."""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from src.single_instance import InstanceAlreadyRunningError, SingleInstanceLock


ROOT = Path(__file__).resolve().parent
CHILDREN = ("run_phase3.py", "run_bot.py")
LOCK = SingleInstanceLock(ROOT / ".pc-promo-monitor.lock")
processes = []


def stop_children(*_):
    for process in processes:
        if process.poll() is None:
            process.terminate()
    for process in processes:
        if process.poll() is None:
            process.wait(timeout=15)


def main():
    environment = os.environ.copy()
    environment["PYTHONUNBUFFERED"] = "1"

    try:
        LOCK.acquire()
    except InstanceAlreadyRunningError as error:
        print(f"Não foi possível iniciar o bot: {error}", file=sys.stderr)
        return 1

    environment["PC_PROMO_SUPERVISOR"] = "1"
    signal.signal(signal.SIGINT, stop_children)
    signal.signal(signal.SIGTERM, stop_children)

    try:
        for script in CHILDREN:
            processes.append(
                subprocess.Popen(
                    [sys.executable, str(ROOT / script)],
                    cwd=ROOT,
                    env=environment,
                )
            )

        while True:
            for process in processes:
                return_code = process.poll()
                if return_code is not None:
                    stop_children()
                    return return_code
            time.sleep(0.5)
    except KeyboardInterrupt:
        stop_children()
        return 0
    finally:
        stop_children()
        LOCK.release()


if __name__ == "__main__":
    raise SystemExit(main())
