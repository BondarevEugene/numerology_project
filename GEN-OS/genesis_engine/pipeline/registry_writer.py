import json
from pathlib import Path


class RegistryWriter:

    def save(self, folder, filename, data):

        path = Path(folder)

        path.mkdir(parents=True, exist_ok=True)

        file = path / filename

        with open(file, "w", encoding="utf8") as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

        return file