import sys

from presidio_analyzer import Pattern, PatternRecognizer, RecognizerRegistry

from dynamic_data_masking.ddm_logger import DynamicDataMaskingLogger

logger = DynamicDataMaskingLogger().get_logger()

class RegistryRecognizerBuilder:
    def __init__(self, language, use_predefined=False):
        self.language = language
        self.use_predefined = use_predefined
        self.recognizer_registry = RecognizerRegistry(supported_languages=[language])
        self.pattern_recognizers = []

    def add_deny_list_patterns(self, deny_list_dict):
        for entity, deny_list in deny_list_dict.items():
            # -------------------------------- TO REFACTOR --------------------------------
            if not deny_list:
                # print(f"{entity} deny list is empty")
                logger.warning(f"TEXT ANALYZER : {entity} DENY TOKENS LIST IS EMPTY")
            # -------------------------------- TO REFACTOR --------------------------------

            else:
                pattern_recognizer = PatternRecognizer(
                    supported_entity=entity, 
                    deny_list=deny_list, 
                    supported_language=self.language
                )
                self.pattern_recognizers.append(pattern_recognizer)

            # -------------------------------- TO REFACTOR --------------------------------
        if not self.pattern_recognizers:
            logger.warning("TEXT ANALYZER : DENY LIST IS EMPTY")
            # print("DENY LIST EMPTY")
            # -------------------------------- TO REFACTOR --------------------------------
        return self

    def add_regex_patterns(self, regex_dict):
        for entity, regex_patterns in regex_dict.items():
            # -------------------------------- TO REFACTOR --------------------------------
            if not regex_patterns:
                logger.warning(f"TEXT ANALYZER : {entity} DENY REGEX LIST IS EMPTY")
                # print(f"{entity} regex list is empty")
            # -------------------------------- TO REFACTOR --------------------------------
            compiled_patterns = [
                Pattern(name=f"{entity}_pattern_{i}", regex=regex, score=1) 
                for i, regex in enumerate(regex_patterns)
            ]
            # -------------------------------- TO REFACTOR --------------------------------
            if not compiled_patterns:
                print(f"NO REGEX FOR {entity} FOUND")
                continue
            # -------------------------------- TO REFACTOR --------------------------------
                
            pattern_recognizer = PatternRecognizer(
                supported_entity=entity, patterns=compiled_patterns, supported_language=self.language
            )
            self.pattern_recognizers.append(pattern_recognizer)
            # -------------------------------- TO REFACTOR --------------------------------
        if not self.pattern_recognizers:
            # print("REGEX LIST EMPTY")
            logger.warning("TEXT ANALYZER : REGEX LIST IS EMPTY")
            # -------------------------------- TO REFACTOR --------------------------------
        return self

    def build(self):
        if self.use_predefined:
            self.recognizer_registry.load_predefined_recognizers()
        if not self.pattern_recognizers:
            logger.error("TEXT ANALYZER : NO RECOGNIZERS FOUND")
            # print('NO RECOGNIZERS FOUND')
            sys.exit()
        for recognizer in self.pattern_recognizers:
            self.recognizer_registry.add_recognizer(recognizer)
        return self.recognizer_registry