from setuptools import setup, find_packages

setup(
    name="ddm_engine",
    version="0.1.0",
    author="Sergiy Polovynko",
    description="A CLI tool for Dynamic Data Masking.",     
    packages=find_packages(),
    install_requires=[
        "argparse",
        "pathlib", 
        "presidio-analyzer", 
        "presidio-anonymizer", 
        "pdfplumber",
        "pytesseract",
        "pyodbc",
        "PyPDF2",
        "reportlab",
        "dotenv"
    ],
    entry_points={
        "console_scripts": [
            "ddm_engine=dynamic_data_masking.main:main",
        ],
    },
    package_data={
        "dynamic_data_masking.ddm_config.analyzer_config": [
            "all-config-C3.yaml",
            "all-config-C4.yaml",
        ],
        "dynamic_data_masking.ddm_config.env_config":[
            ".env"
        ]
    },
    include_package_data=True,
    python_requires=">=3.12",
)
