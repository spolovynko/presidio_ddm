from collections import defaultdict

from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_builder.recognizer_registry import RegistryRecognizerBuilder
from dynamic_data_masking.ddm_connectors.ddm_db_connector import DDMDatabaseReader
from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_builder.nlp_configuration import NLP_CONFIGURATIONS
from dynamic_data_masking.customers import CUSTOMERS
from dynamic_data_masking.ddm_config.config_reader import config
from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_builder.recognizers import RECOGNIZERS

class PresidioAnalyzerDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct(self, from_config_file, language, use_predefined, customer):
        if from_config_file:
            if use_predefined:
                print('form config file using C3')
                config_file = r'dynamic_data_masking\ddm_config\analyzer_config\all-config-C3.yaml'
            else:
                print('form config file using oly C4')
                config_file = r'dynamic_data_masking\ddm_config\analyzer_config\all-config-C4.yaml'

            self.builder.set_config_file(config_file)
            return self.builder.build_analyzer()
        
        else:
            if language not in NLP_CONFIGURATIONS:
                print(f"Warning: Language '{language}' not found, defaulting to English.")
                language = "en"

            configuration = NLP_CONFIGURATIONS[language]
            recognizer_data = RECOGNIZERS.get(language, {'deny_list': {}, 'regex_list': {}})
            
            # ----------------------------------- DATABASE INTEGRATION MVP 1 ---- TO REFACTOR -----------------------------------
            recognizer_data = defaultdict(list)
            recognizer_data['deny_list'] = {}
            recognizer_data['regex_list'] = {}

            server = config.get("SERVER")
            database = config.get("DATABASE")

            customer_data = CUSTOMERS.get(customer)
            
            db_connection = DDMDatabaseReader(
                server=server,
                db=database
            )

            db_connection.connect_to_server()

            for category in customer_data['c4_deny_list_categories']:
                query = db_connection.select_deny_list_query(
                    category=category,
                    language=language,
                    values_table='ddm_deny_list',
                    col_name='value'
                )
                result = db_connection.execute_query(query=query)
                tokens = [token[0] for token in result]
                recognizer_data["deny_list"][category] = tokens
                

            for category in customer_data['c4_regex_list_categories']:
                query = db_connection.select_deny_list_query(
                    category=category,
                    language=language,
                    values_table='ddm_regex_list',
                    col_name='regex'
                )
                result = db_connection.execute_query(query=query)
                tokens = [token[0] for token in result]
                recognizer_data["regex_list"][category] = tokens

            recognizer_data = dict(recognizer_data)
            # ----------------------------------- DATABASE INTEGRATION MVP 1 ---- TO REFACTOR -----------------------------------
            recognizer_builder = RegistryRecognizerBuilder(language=language, use_predefined=use_predefined)
            recognizer_registry = (
                recognizer_builder
                .add_deny_list_patterns(recognizer_data['deny_list'])
                .add_regex_patterns(recognizer_data['regex_list'])
                .build()
            )

            self.builder.set_nlp_configuration(configuration)
            self.builder.set_recognizer_registry(recognizer_registry)
            return self.builder.build_analyzer()
