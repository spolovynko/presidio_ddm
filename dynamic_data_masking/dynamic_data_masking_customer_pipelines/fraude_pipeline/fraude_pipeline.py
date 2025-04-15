import sys
import json
import os

from pathlib import Path

from dynamic_data_masking.dynamic_data_masking_pipeline.dynamic_data_masking_pipeline import *
from dynamic_data_masking.ddm_connectors.ddm_db_connector import DDMDatabaseReader
from dynamic_data_masking.ddm_logger import DynamicDataMaskingLogger
from dynamic_data_masking.utils import find_file
from dynamic_data_masking.ddm_config.config_reader import config
from dynamic_data_masking.dynamic_data_masking_pipeline.mappers import LANG_MAP, CONF_LEVEL_MAP, ANALYZER, ANONYMIZER

def fraude_pipeline(event):
    customer = 'fraude'
    # LOGGER INSTANTIATION
    logger = DynamicDataMaskingLogger().get_logger()
    logger.info('DDM ENGINE INSTANTIATED - FRAUDE CUSTOMER')


    # ARGS FROM .ENV
    server = config.get("SERVER")
    database = config.get("DATABASE")
    resolution = int(config.get('RESOLUTION'))
    ocr_config = config.get("OCR_CONFIG")
    analyzer_engine = config.get('ANALYZER_ENGINE')
    masking_strategy = config.get('MASKING_STRATEGY')


    # ARGS FROM DB
    db_connection = DDMDatabaseReader(
                server=server,
                db=database
            )

    input_folder = db_connection.select_params('input_kafka_folder')
    base_input_folder = db_connection.execute_query(input_folder)[0][0]
    full_input_path = os.path.join(base_input_folder, event)
    input_pdf_file = find_file(full_input_path, '.pdf')
    file_name = Path(input_pdf_file).stem
    input_md_file = find_file(full_input_path, '.json')

    output_folder = db_connection.select_params('output_kafka_folder')
    base_output_folder = db_connection.execute_query(output_folder)[0][0]
    full_output_path = os.path.join(base_output_folder, event)
    output_pdf_file = os.path.join(full_output_path, f"{file_name}_REDACTED.pdf")
    output_md_file = os.path.join(full_output_path, "metadata.json")

    
    

    # ARGS FROM MD
    with open(input_md_file, "r") as file:
        metadata = json.load(file)

    try:
        metadata['fileName'] = Path(output_pdf_file).name
        metadata["outputConfidentialityRating"] = 'C4'
        
        language = metadata.get("fileLanguage")
        file_name = Path(input_pdf_file).name
        # LOGGIMG DDM PARAMS:
        logger.info(
            f'DDM PARAMS: File Name: {file_name}; Language : {language}; Image reader resolustion : {resolution} pixels; Customer : {customer}; Masking confidentiality level : c4; Analyzer Engine : {analyzer_engine}; Masking strategy : {masking_strategy}')

    
        if language not in LANG_MAP:
            
            print(f'LANGUAGE {language} is not supported by dynamic data masking engine')
            logger.warning(f"Language {language} not supported")
                
        pipeline = DynamicDataMaskingPipeline()

        pipeline.add_step(FileProcessorStep(
            file_path=input_pdf_file, 
            language=LANG_MAP[language], 
            resolution=resolution, 
            ocr_config=ocr_config
            )
        )
        pipeline.add_step(AnalyzerStep(
            from_config_file=ANALYZER[analyzer_engine],
            language=language,
            customer=customer,
            use_predefined=CONF_LEVEL_MAP['c4']
            )
        )
        pipeline.add_step(AnonymizerStep(
            use_default_operators=ANONYMIZER['yes']
            )
        )

        pipeline.add_step(RedactorStep(
            redaction_strategy=masking_strategy,
            input_file_path=input_pdf_file, 
            output_pdf_path=output_pdf_file
            )
        )
        try:
            data = pipeline.execute_pipeline()
            message = "Data masking run completed succesfully"
            metadata['status'] = data['status']
            metadata['message'] = message

        except:
            status = 403
            message = "Data masking run failed"
            metadata['status'] = status
            metadata['message'] = message
        
    except:
        print("error")
        status = 403
        message = "Data masking run failed"
        metadata['status'] = status
        metadata['message'] = message
        

    with open(output_md_file, "w") as file:
        json.dump(metadata, file)
