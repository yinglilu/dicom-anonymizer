
[![Python package](https://github.com/yinglilu/dicom-anonymizer/actions/workflows/pythonpackage.yml/badge.svg)](https://github.com/yinglilu/dicom-anonymizer/actions/workflows/pythonpackage.yml)


# Anonymize dicom files in input_dir recursively

## Usage: 

to anonymize a file:  

    python dcm_anon.py path/to/input_dicom_file path/to/output_dicom_file

to anonymize all dicom files in a folder recursively:    

    python dcm_anon.py input_dir output_dir


## Note:

`dcm_anon.py` follows the BASIC APPLICATION LEVEL CONFIDENTIALITY PROFILE:http://dicom.nema.org/Dicom/supps/sup55_03.pdf


## License
The source code for the site is licensed under the MIT license, which you can find in the MIT-LICENSE.txt file.