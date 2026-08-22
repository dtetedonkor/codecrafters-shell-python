import readline
import os
import subprocess


class Completer:
    def __init__(self):
        self.BUILTIN = ["cd", "pwd", "type", "exit", "echo", "complete","jobs"]
        self.completions = {}

        # readline calls completer(text, 0), (text, 1), ... for a single TAB
        # press. We compute the full match list once at state == 0 and just
        # index into it afterwards, instead of rescanning PATH / the
        # filesystem / re-running a subprocess on every single call.
        self._matches: list[str] = []

        # PATH rarely changes mid-session, so the executable scan is cached
        # across completions too. Call refresh_path_cache() if PATH changes.
        self._exec_cache: set[str] | None = None

    def refresh_path_cache(self) -> None:
        """Force a rescan of PATH on the next completion request."""
        self._exec_cache = None

    # Never treat these as runnable commands even if the filesystem reports
    # them as "executable" (common on WSL /mnt/c PATH dirs that mix real
    # Windows binaries with .dll, .manifest, .config, etc.).
    _EXCLUDED_EXTENSIONS = {
        ".dll", ".manifest", ".config", ".ini", ".log", ".pdb",
        ".lib", ".a", ".o", ".obj", ".json", ".xml", ".md", ".txt",
    }

    # Extensions Windows itself treats as directly runnable. Used as the
    # fallback allow-list for WSL-mounted drives when PATHEXT isn't set.
    _WINDOWS_EXEC_EXTENSIONS = {".exe", ".bat", ".cmd", ".com", ".ps1", ".msi"}

    @staticmethod
    def _is_windows_mount(dir_str: str) -> bool:
        """True for WSL-mounted Windows drives like /mnt/c, /mnt/d, ...

        Files under these paths are served through DrvFs, which doesn't
        carry real Unix permission bits -- os.access(X_OK) ends up true
        for nearly everything (.dll, .manifest, plain text files, ...).
        So for these directories we filter by extension instead of trusting
        the executable bit.
        """
        parts = os.path.normpath(dir_str).split(os.sep)
        # normpath("/mnt/c/Windows/System32") -> ["", "mnt", "c", "Windows", "System32"]
        return len(parts) >= 3 and parts[1] == "mnt" and len(parts[2]) == 1

    def get_posix_executables(self) -> set[str]:
        if self._exec_cache is not None:
            return self._exec_cache

        # Respect PATHEXT if WSL interop has exported it from Windows;
        # otherwise fall back to the standard Windows executable extensions.
        pathext = os.environ.get("PATHEXT")
        win_allowed_ext = (
            {ext.lower() for ext in pathext.split(os.pathsep)}
            if pathext
            else self._WINDOWS_EXEC_EXTENSIONS
        )

        executables = set()
        for dir_str in os.get_exec_path():
            is_win_mount = self._is_windows_mount(dir_str)

            try:
                with os.scandir(dir_str) as it:
                    for entry in it:
                        ext = os.path.splitext(entry.name)[1].lower()

                        if ext in self._EXCLUDED_EXTENSIONS:
                            continue

                        if is_win_mount:
                            # DrvFs: trust the extension, not X_OK.
                            if ext not in win_allowed_ext:
                                continue
                        else:
                            try:
                                if not (entry.is_file() and os.access(entry.path, os.X_OK)):
                                    continue
                            except OSError:
                                continue

                        executables.add(entry.name)
            except OSError:
                continue

        self._exec_cache = executables
        return executables

    @staticmethod
    def _scan_dir(path="."):
        """Return (files, dirs) directly under `path` in a single pass,
        using scandir's cached dirent info instead of separate
        listdir + isfile/isdir stat calls per entry."""
        files, dirs = set(), set()
        try:
            with os.scandir(path) as it:
                for entry in it:
                    try:
                        if entry.is_dir():
                            dirs.add(entry.name)
                        elif entry.is_file():
                            files.add(entry.name)
                    except OSError:
                        continue
        except OSError:
            pass
        return files, dirs

    def _complete_custom(self, command, current_word, previous_word, comp_line, comp_point):
        script = self.completions[command]
        env = os.environ.copy()
        env["COMP_LINE"] = comp_line
        env["COMP_POINT"] = str(comp_point)

        try:
            proc = subprocess.run(
                [script, command, current_word, previous_word],
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
        except (subprocess.CalledProcessError, OSError):
            return []

        candidates = set(proc.stdout.splitlines())
        return sorted(c.rstrip() for c in candidates if c.startswith(current_word))

    def _build_matches(self, text: str) -> list[str]:
        comp_line = readline.get_line_buffer()
        parts = comp_line.split()
        if not parts:
            return []

        last_str = comp_line.rsplit(" ", 1)[-1]
        command = parts[0]
        comp_point = len(comp_line.encode("utf-8"))

        # -----------------------------------
        # Custom completion: complete -C
        # -----------------------------------
        if command in self.completions:
            if comp_line.endswith(" "):
                current_word = ""
                previous_word = parts[-1] if len(parts) >= 2 else ""
            else:
                current_word = parts[-1]
                previous_word = parts[-2] if len(parts) >= 2 else ""

            options = self._complete_custom(
                command, current_word, previous_word, comp_line, comp_point
            )
            if not options:
                print("\x07", end="", flush=True)
            return [opt + " " for opt in options]

        # -----------------------------------
        # Completing a path (contains "/")
        # -----------------------------------
        if "/" in last_str:
            path, prefix = last_str.rsplit("/", 1)
            files, dirs = self._scan_dir(path or "/")  # "/usr" -> path="" -> use "/"
            entries = files | dirs
            options = sorted(e for e in entries if e.startswith(prefix))
            return [e + "/" if e in dirs else e + " " for e in options]

        # -----------------------------------
        # Completing a filename/directory (not first word)
        # -----------------------------------
        if " " in comp_line:
            files, dirs = self._scan_dir(".")
            entries = files | dirs
            options = sorted(e for e in entries if e.startswith(last_str))
            return [e + "/" if e in dirs else e + " " for e in options]

        # -----------------------------------
        # Completing commands (first word)
        # -----------------------------------
        commands = set(self.BUILTIN) | self.get_posix_executables()
        return sorted(c + " " for c in commands if c.startswith(text))

    def completer(self, text: str, state: int):
        if state == 0:
            self._matches = self._build_matches(text)

        if state >= len(self._matches):
            return None

        return self._matches[state]