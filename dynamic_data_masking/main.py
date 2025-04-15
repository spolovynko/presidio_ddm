import argparse
import sys

from dynamic_data_masking.dynamic_data_masking_customer_pipelines import fraude_pipeline
from dynamic_data_masking.ddm_logger import DynamicDataMaskingLogger

def main():

    logger = DynamicDataMaskingLogger().get_logger()

    # ------------------------------------------ TO REFACTOR ------------------------------------------

    CUSTOMERS = {
        'fraude': fraude_pipeline
        }
    # ------------------------------------------ TO REFACTOR ------------------------------------------

    parser = argparse.ArgumentParser(description="Arguments parser for dynamic data masking engine")

    parser.add_argument("--event", type=str, help="kafka event number")
    parser.add_argument("--customer", type=str, default="fraude",help="DDM customer")

    # ---------------------------------------- ADD ARGUMENTS WHEN NEEDED ------------------------------------------
    args = parser.parse_args()

    if args.customer not in CUSTOMERS:
        
        print(f'Customer not found')
        logger.warning(f'Customer {args.customer} not supported')
        sys.exit()

    pipeline = CUSTOMERS.get(args.customer)
    pipeline(args.event)

if __name__ == "__main__":
    main()