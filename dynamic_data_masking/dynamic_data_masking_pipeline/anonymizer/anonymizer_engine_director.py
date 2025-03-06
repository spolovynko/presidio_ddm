from dynamic_data_masking.dynamic_data_masking_pipeline.anonymizer.anonimyzer_engine_builder import AnonymizerEngineBuilder, OperatorConfigBuilder

class AnonymizerEngineDirector:
    
    @staticmethod
    def build_anonymizer(use_default_operators=False):
        builder = AnonymizerEngineBuilder()

        if use_default_operators:
            # Define operators dynamically inside the Director
            person_operator = OperatorConfigBuilder("replace").with_param("new_value", "<REDACTED>").build()
            phone_operator = OperatorConfigBuilder("redact").build()

            # Add them to the builder
            builder.add_operator("PERSON", person_operator)
            builder.add_operator("PHONE_NUMBER", phone_operator)

        return builder.build()

    @staticmethod
    def build_custom_anonymizer(custom_operator_name, custom_operator_class, use_default_operators=True):
        builder = AnonymizerEngineBuilder()

        # Optionally add default operators
        if use_default_operators:
            person_operator = OperatorConfigBuilder("replace").with_param("new_value", "<REDACTED>").build()
            builder.add_operator("PERSON", person_operator)

        # Add the custom operator
        builder.add_custom_operator(custom_operator_name, custom_operator_class)

        return builder.build()

