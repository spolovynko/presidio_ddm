pip uninstall ddm_engine -y
python .\setup.py bdist_wheel
pip install .\dist\ddm_engine-0.1.0-py3-none-any.whl