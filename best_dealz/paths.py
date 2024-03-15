from pathlib import Path


class Paths:
    def __init__(self, working_dir: Path) -> None:
        self.working_dir = working_dir.resolve()
        self.home_dir: Path = Path.home()
        self.cache_dir = self.home_dir / ".cache" / "dealz"
        self.config = self.cache_dir / "config.yml"
