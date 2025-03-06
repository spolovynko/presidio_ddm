from abc import ABC, abstractmethod
from pathlib import Path

class ContentExtractor(ABC):
    """Abstract base class for file processing."""

    def __init__(self, file_path, language, resolution, ocr_config):
        self.file_path = Path(file_path)
        self.language = language
        self.resolution = resolution
        self.ocr_config = ocr_config

    @abstractmethod
    def process(self):
        """Abstract method to be implemented for processing files."""
        pass