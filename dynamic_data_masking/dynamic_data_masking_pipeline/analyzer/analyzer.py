from dynamic_data_masking.ddm_logger import DynamicDataMaskingLogger
from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_builder import PresidioAnalyzerBuilder, PresidioAnalyzerEngineProviderBuilder
from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_director import PresidioAnalyzerDirector

logger = DynamicDataMaskingLogger().get_logger()

class DynamicDataMaskingAnalyzer:
    
    def __init__(self, from_config_file, language, customer, use_predefined):
        self.from_config_file = from_config_file
        self.language = language
        self.use_predefined = use_predefined
        
        if self.from_config_file:
            self.builder = PresidioAnalyzerEngineProviderBuilder()
            logger.info(f"TEXT ANALYZER : ANALYZER CONFIGURATION FROM YAML FILE")

        else: 
            self.builder = PresidioAnalyzerBuilder(language=self.language)
            logger.info(f"TEXT ANALYZER : ANALYZER CONFIGURATION FROM CODE")

        self.director = PresidioAnalyzerDirector(self.builder)
        self.customer = customer

        self.analyzer = self.director.construct(
            from_config_file=self.from_config_file,
            language=self.language,
            customer=self.customer, 
            use_predefined=self.use_predefined
            )
        logger.info(f"TEXT ANALYZER : ANALYZER ENGINE READY")
        logger.info(f"TEXT ANALYZER : PARAMS : Analyzer configuration from config file : {self.from_config_file}; Language : {self.language}; Customer : {self.customer}; Use of predefined recognizers : {self.use_predefined}")
    def analyze_text(self, text):

        return self.analyzer.analyze(text=text, language=self.language)
