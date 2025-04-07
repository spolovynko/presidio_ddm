import sys

from pathlib import Path

from dynamic_data_masking.ddm_logger import DynamicDataMaskingLogger
from dynamic_data_masking.dynamic_data_masking_pipeline.file_processor.content_extractor.pdf_extractor import PDFProcessor

logger = DynamicDataMaskingLogger().get_logger()

class DynamicDataMaskingFileProcessor:
    """Determines the correct processing function based on file type."""

    def __init__(self, file_path, language, resolution, ocr_config):
        self.supported_types = {
            '.pdf': PDFProcessor
            # '.jpg': ,  # Future expansion
            # '.email': ,    # Future expansion
        }
        self._resolution = None
        self._file_path = None

        self.file_path = file_path  # Triggers setter + validation
        self._resolution = resolution
        self.language = language
        self.ocr_config = ocr_config
    
### ---------------------------------- ADD LOGGER ----------------------------------
### ---------------------------------- ADD DB PROCESSING LOGGER ----------------------------------
    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        path = Path(value)

        if not path.is_file():
            # print(f"❌ File not found: '{value}'")
            logger.error(f"FILE READER : {value} file not found")
            sys.exit(1)

        ext = path.suffix.lower()
        if ext not in self.supported_types:
            # print(f"❌ Unsupported file type: '{ext}'. Supported types: {', '.join(self.supported_types.keys())}")
            logger.error(f"FILE READER : File extension {ext} not supported")
            sys.exit(1)
        
        self._file_path = path


    @property
    def file_extension(self):
        return self._file_path.suffix.lower() if self._file_path else None
    

    @property
    def resolution(self):
        return self._resolution
    

    @resolution.setter
    def resolution(self, value):
        if not isinstance(value, int):
            print(f"❌ Resolution must be an integer. Got:{value}")
            

        if not (350 <= value <= 800):
            # print(f"❌ Resolution must be an between 350 and 800. Got:{value}")
            logger.error(f"FILE READER : FILE READER RESOLUTION {value}, must be between 350 and 800 ")
### ---------------------------------- ADD LOGGER ----------------------------------
### ---------------------------------- ADD DB PROCESSING LOGGER ----------------------------------


    def process(self):
        """Determines and executes the correct processing function."""
        processor_class = self.supported_types[self.file_extension]
        logger.info(f"FILE READER : READING {self.file_extension} FILE")
        processor = processor_class(
            self.file_path,
            self.language,
            self.resolution,
            self.ocr_config
        )
        return processor.process()
