from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    history_file_path: str
    future_file_path: str