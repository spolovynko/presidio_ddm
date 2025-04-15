from abc import ABC, abstractmethod
import sys

from dynamic_data_masking.dynamic_data_masking_pipeline.file_processor import DynamicDataMaskingFileProcessor
from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer import DynamicDataMaskingAnalyzer
from dynamic_data_masking.dynamic_data_masking_pipeline.anonymizer import DynamicDataMaskingAnonimyzer
from dynamic_data_masking.dynamic_data_masking_pipeline.file_redactor import DynamicDataMaskingFileRedactor
from dynamic_data_masking.ddm_logger import DynamicDataMaskingLogger

logger = DynamicDataMaskingLogger().get_logger()

class PipelineStep(ABC):
    
    @abstractmethod
    def execute(self, data):
        pass

class FileProcessorStep(PipelineStep):
    def __init__(self, file_path, language, resolution, ocr_config):
        self.file_path = file_path
        self.language = language
        self.resolution = resolution
        self.ocr_config = ocr_config

    def execute(self, data=None):
        logger.info("FILE READER : RUNS")

        file_processor = DynamicDataMaskingFileProcessor(
            file_path=self.file_path, 
            language=self.language, 
            resolution=self.resolution,
            ocr_config=self.ocr_config
            )
        try:
            extracted_text, word_coordinates = file_processor.process()
            logger.info('FILE READER : TEXT EXTRACTED SUCESSFULLY; TOKENS COORDINATES EXTRACTED SUCCESSFULLY')
        except:
            logger.error('FILE READER : FAILURE TO EXTRACT TEXT')
        return {"text": extracted_text, "word_coordinates": word_coordinates, "status":200}


class AnalyzerStep(PipelineStep):
    def __init__(self, from_config_file, language, customer, use_predefined):
        self.language = language
        self.customer = customer
        self.use_predefined = use_predefined
        self.from_config_file = from_config_file

    def execute(self, data):
        # print("ANALYZER RUNS")
        logger.info("TEXT ANALYZER : RUNS")

        analyzer = DynamicDataMaskingAnalyzer(
            from_config_file = self.from_config_file,
            language = self.language,
            customer = self.customer,
            use_predefined=self.use_predefined
            )
        try:
            logger.info("TEXT ANALYZER : ANALYZIS RUNS")
            result = analyzer.analyze_text(text=data["text"])
            logger.info("TEXT ANALYZER : ANALYZIS COMPLETE")
            # ----------------------------------------------- TO REFACTOR -----------------------------------------------
            text = data['text']
            results = [(res.entity_type, text[res.start:res.end]) for res in result]
            logger.info(f"TEXT ANALYZER : ANALYZIS RESULTS : {results}")
        except ValueError:
            logger.error("TEXT ANALYZER : FAILURE TO ANALYZE")
        data["analysis_results"] = result
        data['status'] = 404
        return data
    
class AnonymizerStep(PipelineStep):

    def __init__(self, use_default_operators):
        self.use_default_operators = use_default_operators

    def execute(self, data):
        # print("ANONYMIZER RUNS")
        logger.info("TEXT ANONYMISATION : RUNS")

        anonymizer = DynamicDataMaskingAnonimyzer()
        masked_text = anonymizer.anonimyze(
            text=data["text"], 
            analyzer_results=data["analysis_results"], 
            use_default_operators=self.use_default_operators
            )
        logger.info("TEXT ANONIMYZATION : ANONYMIZATION COMPLETED")
        data["masked_text"] = masked_text
        return data
    
class RedactorStep(PipelineStep):
    def __init__(self, input_file_path, output_pdf_path, redaction_strategy):
        self.input_file_path = input_file_path
        self.output_pdf_path = output_pdf_path
        self.redaction_strategy = redaction_strategy
        
    def execute(self, data):
        # print("REDACTOR RUNS")
        logger.info("FILE MASKING : RUNS")

        redactor = DynamicDataMaskingFileRedactor(redaction_strategy=self.redaction_strategy)
        try:
            redactor.redact_file(
                input_file_path=self.input_file_path,
                extracted_text=data["text"],
                masked_text=data["masked_text"],
                words_info=data["word_coordinates"],
                output_pdf_path=self.output_pdf_path
            )
            logger.info("FILE MASKING : FILE SUCESSFULLY REDACTED")
        except:
            logger.error("FILE MASKING : FILE MASKING FAILED")
            data['status'] = 404
        return data

class DynamicDataMaskingPipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def execute_pipeline(self, initial_data=None):
        data = initial_data
        for step in self.steps:
            data = step.execute(data)
        return data


