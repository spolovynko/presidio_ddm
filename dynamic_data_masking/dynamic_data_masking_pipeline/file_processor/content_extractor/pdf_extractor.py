import pdfplumber

from dynamic_data_masking.ddm_logger import DynamicDataMaskingLogger
from dynamic_data_masking.dynamic_data_masking_pipeline.file_processor.content_extractor import ContentExtractor
from dynamic_data_masking.dynamic_data_masking_pipeline.file_processor.image_processor import ImageTextProcessor, ImageCoordinateProcessor, PageToImageConverter

logger = DynamicDataMaskingLogger().get_logger()

class PDFProcessor(ContentExtractor):
    """Handles PDF processing, extracting text and word coordinates."""

    def __init__(self, file_path, language, resolution, ocr_config):
        super().__init__(file_path, language, resolution, ocr_config)
        self.text_processor = ImageTextProcessor()
        self.coord_processor = ImageCoordinateProcessor()

    def process(self):
        """Processes a PDF and extracts text along with word coordinates."""
        extracted_text = ""
        all_word_data = []

        with pdfplumber.open(self.file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):

                logger.info(f"FILE READER : CONVERTING PAGE {page_num} out of {len(pdf.pages)}")

                image = PageToImageConverter.convert(page, resolution=self.resolution)

                logger.info(f"FILE READER : PAGE {page_num} CONVERTED TO IMAGE")

                # Extract Text
                logger.info(f"FILE READER : TEXT EXTRACTED FROM PAGE {page_num}")

                page_text = self.text_processor.process(image, lang=self.language, ocr_config=self.ocr_config)
                extracted_text += page_text

                
                # Extract Word Coordinates
                word_data = self.coord_processor.process(image, page, page_num, lang=self.language)

                logger.info(f"FILE READER : TOKEN COORDINATES RECORDER FROM PAGE {page_num}")

                all_word_data.extend(word_data)

        return extracted_text, all_word_data