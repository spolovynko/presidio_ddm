import argparse
import sys

from pathlib import Path

from dynamic_data_masking.dynamic_data_masking_pipeline.dynamic_data_masking_pipeline import *
from dynamic_data_masking.ddm_logger import DynamicDataMaskingLogger
from dynamic_data_masking.dynamic_data_masking_pipeline.mappers import LANG_MAP, CONF_LEVEL_MAP, ANALYZER, ANONYMIZER
from dynamic_data_masking.customers import CUSTOMERS

def main():
    # LOGGER INSTANTIATION
    logger = DynamicDataMaskingLogger().get_logger()
    logger.info('DDM ENGINE INSTANTIATED')

    parser = argparse.ArgumentParser(description="Arguments parser for dynamic data masking engine")
    # FILE PROCESSOR STEP ARGUMENTS
    parser.add_argument("input_file_path", help='path to the file required masking')
    parser.add_argument("--lang", type=str, default='en', help='language of the file')
    parser.add_argument("--resolution", type=int, default=350, help="resolution for input file reading")
    parser.add_argument("--ocr-config", type=str, default='--oem 3 --psm 6', help='provides configuration for content extraction from file using OCR (Object Character Recognition)')

    # TEXT ANALYZER STEP ARGUMENTS
    parser.add_argument("--conf_level", type=str, default='c4', choices=['c3','c4'])
    parser.add_argument("--analyzer_engine", type=str, default='from_config_file', choices=['from_config_file', 'from_code'], help='provides the option on Analyzer Engine builder code / from config file')
    parser.add_argument("--customer", type=str, default='fraude', choices=CUSTOMERS.keys(), help='list of customers')
    # TEXT ANONYMIZER STEP ARGUMETNS
    parser.add_argument("--anonimyzer_operator", type=str, default='yes', help='type of anonimyzer')

    # FILE REDACTOR STEP ARGUMENTS
    parser.add_argument("--masking_strategy", default="blackout", help="Masking strategy for masking data")
    parser.add_argument("--output_file_path", help="path to where the masked file will be generated")

    # PARSING ARGUMENTS
    args = parser.parse_args()
    file_name = Path(args.input_file_path).name
    
    # LOGGIMG DDM PARAMS:
    logger.info(
        f'DDM PARAMS: File Name: {file_name}; Language : {args.lang}; Image reader resolustion : {args.resolution} pixels; Customer : {args.customer}; Masking confidentiality level : {args.conf_level}; Analyzer Engine : {args.analyzer_engine}; Masking strategy : {args.masking_strategy}')

    ### ---------------------------------- TO REFACTOR ----------------------------------
    ### ---------------------------------- ADD LOGGER ----------------------------------
    ### ---------------------------------- ADD DB PROCESSING LOGGER ----------------------------------
    
    if args.lang not in LANG_MAP:
        
        print(f'LANGUAGE {args.lang} is not supported by dynamic data masking engine')
        logger.warning(f"Language {args.lang} not supported")
        sys.exit()
    
    if args.customer not in CUSTOMERS:
        
        print(f'Customer not found')
        logger.warning(f'Customer {args.customer} not supported')
        sys.exit()

    ### ---------------------------------- TO REFACTOR ----------------------------------
    ### ---------------------------------- ADD LOGGER ----------------------------------
    ### ---------------------------------- ADD DB PROCESSING LOGGER ----------------------------------
         
    pipeline = DynamicDataMaskingPipeline()
    pipeline.add_step(FileProcessorStep(
        file_path=args.input_file_path, 
        language=LANG_MAP[args.lang], 
        resolution=args.resolution, 
        ocr_config=args.ocr_config
        )
    )
    pipeline.add_step(AnalyzerStep(
        from_config_file=ANALYZER[args.analyzer_engine],
        language=args.lang,
        customer=args.customer,
        use_predefined=CONF_LEVEL_MAP[args.conf_level]
        )
    )
    pipeline.add_step(AnonymizerStep(
        use_default_operators=ANONYMIZER[args.anonimyzer_operator]
        )
    )

    pipeline.add_step(RedactorStep(
        redaction_strategy=args.masking_strategy,
        input_file_path=args.input_file_path, 
        output_pdf_path=args.output_file_path
        )
    )

    pipeline.execute_pipeline()

if __name__ == "__main__":
    main()