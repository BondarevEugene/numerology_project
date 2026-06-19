from pathlib import Path


class Downloader:

    def __init__(self, provider):
        self.provider = provider

    def run(self):

        print(f"Downloading from {self.provider.name}")

        data = self.provider.download()

        return data