from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_builder import PresidioAnalyzerBuilder, PresidioAnalyzerEngineProviderBuilder
from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_director import PresidioAnalyzerDirector

class DynamicDataMaskingAnalyzer:
    
    def __init__(self, from_config_file, language, customer, use_predefined):
        self.from_config_file = from_config_file
        self.language = language
        self.use_predefined = use_predefined
        
        if self.from_config_file:
            print('Analyzer configured from yaml')
            self.builder = PresidioAnalyzerEngineProviderBuilder()
        else: 
            print('Analyzer configured from code')
            self.builder = PresidioAnalyzerBuilder(language=self.language)

        self.director = PresidioAnalyzerDirector(self.builder)
        self.customer = customer

        self.analyzer = self.director.construct(
            from_config_file=self.from_config_file,
            language=self.language,
            customer=self.customer, 
            use_predefined=self.use_predefined
            )

    def analyze_text(self, text):
        return self.analyzer.analyze(text=text, language=self.language)
