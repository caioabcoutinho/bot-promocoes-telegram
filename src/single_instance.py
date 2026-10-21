"""Prevent concurrent bot processes from sharing Telegram session files."""

import errno
import os
from pathlib import Path


class InstanceAlreadyRunningError(RuntimeError):
    """Raised when another bot process owns the application lock."""


class SingleInstanceLock:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._acquired = False

    def acquire(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(
                self.path,
                os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            )
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise
            owner_pid = self._read_owner_pid()
            if owner_pid and self._process_exists(owner_pid):
                raise InstanceAlreadyRunningError(
                    f"já existe outra instância em execução (PID {owner_pid})"
                )
            self.path.unlink(missing_ok=True)
            return self.acquire()

        with os.fdopen(descriptor, "w", encoding="ascii") as lock_file:
            lock_file.write(str(os.getpid()))
        self._acquired = True

    def release(self):
        if not self._acquired:
            return
        self.path.unlink(missing_ok=True)
        self._acquired = False

    def _read_owner_pid(self):
        try:
            return int(self.path.read_text(encoding="ascii").strip())
        except (FileNotFoundError, ValueError, OSError):
            return None

    @staticmethod
    def _process_exists(pid):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True
