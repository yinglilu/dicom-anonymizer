#!/usr/bin/env python3

# anonymize dicom files in input_dir recursively
# follow the BASIC APPLICATION LEVEL CONFIDENTIALITY PROFILE:http://dicom.nema.org/Dicom/supps/sup55_03.pdf
#
# usage: # python dcm_anon.py input_dir output_dir

# Author: YingLi Lu
# Email: yinglilu@gmail.com
# Date: 2018-07-24
# Update: Oct 3, 2023
# Ver: 0.2

import os
import sys
import pydicom


date_anon = "18000101"
date_tags = ("StudyDate", "PatientBirthDate")

age_anon = "000Y"
age_tags = ("PatientAge",)

decimal_anon = "0"
decimal_tags = ("PatientSize", "PatientWeight")

code_anon = "O"  ## M/F->O
code_tags = ("PatientSex",)

string_anon = "anon"
# leave "SeriesDescription" untouchED, since it might be needed for BIDS etc.
string_tags = (
    "StudyDescription",
    "PatientName",
    "PatientID",
    "PatientBirthTime",
    "OtherPatientIDs",
    "OtherPatientNames",
    "EthnicGroup",
    "PatientComments",
    "ReferringPhysicianName",
    "StudyID",
    "AccessionNumber",
    "PhysiciansOfRecord",
    "NameOfPhysiciansReadingStudy",
    "AdmittingDiagnosesDescription",
    "Occupation",
    "AdditionalPatientHistory",
    "PerformingPhysicianName",
    "ProtocolName",
    "OperatorsName",
    "InstitutionName",
    "InstitutionAddress",
    "StationName",
    "InstitutionalDepartmentName",
    "DeviceSerialNumber",
    "DerivationDescription",
    "ImageComments",
)

StudyInstanceUID_dict = {}
SeriesInstanceUID_dict = {}

tags2anon = {
    date_tags: date_anon,
    age_tags: age_anon,
    decimal_tags: decimal_anon,
    code_tags: code_anon,
    string_tags: string_anon,
}


def anonymize_and_save(dicom_file, dest_dicom_file, tags2anon):
    try:
        ds = pydicom.dcmread(dicom_file, stop_before_pixels=False)
    except:
        raise

    for tags, anon in tags2anon.items():
        for tag in tags:
            if tag in ds:
                print(f"{tag}: {ds[tag].value} -> {anon}")
                ds[tag].value = anon

    # keep same StudyInstanceUID/SeriesInstanceUID for each study/series
    # modify StudyInstanceUID
    if "StudyInstanceUID" in ds:
        if ds.StudyInstanceUID in StudyInstanceUID_dict:
            ds.StudyInstanceUID = StudyInstanceUID_dict[ds.StudyInstanceUID]
        else:
            StudyInstanceUID_dict[ds.StudyInstanceUID] = pydicom.uid.generate_uid()
            ds.StudyInstanceUID = StudyInstanceUID_dict[ds.StudyInstanceUID]

    # modify SeriesInstanceUID
    if "SeriesInstanceUID" in ds:
        if ds.SeriesInstanceUID in SeriesInstanceUID_dict:
            ds.SeriesInstanceUID = SeriesInstanceUID_dict[ds.SeriesInstanceUID]
        else:
            SeriesInstanceUID_dict[ds.SeriesInstanceUID] = pydicom.uid.generate_uid()
            ds.SeriesInstanceUID = SeriesInstanceUID_dict[ds.SeriesInstanceUID]

    try:
        ds.save_as(dest_dicom_file)
    except:
        raise


usage = """usage:
    to anonymize a file:
        python dcm_anon.py path/to/input_dicom_file path/to/output_dicom_file
    to anonymize all dicom files in a folder recursively:  
        python dcm_anon.py input_dir output_dir
    """


def main():
    if len(sys.argv) != 3:
        sys.exit(usage)

    if not os.path.exists(sys.argv[1]):
        sys.exit(f"error: {sys.argv[1]} not exist.")

    # handle `python dcm_anon.py input_dicom output_dicom`
    if os.path.isfile(sys.argv[1]):
        if os.path.exists(sys.argv[2]) and os.path.isdir(sys.argv[2]):
            sys.exit(f"error: {sys.argv[1]} is file, but {sys.argv[2]} is a folder.")

        # output is path/to/dicom_file
        output_full_filename = os.path.join(os.getcwd(), sys.argv[2])
        output_full_dir = os.path.dirname(output_full_filename)
        if not os.path.exists(output_full_dir):
            os.makedirs(output_full_dir)

        try:
            anonymize_and_save(sys.argv[1], output_full_filename, tags2anon)
        except pydicom.errors.InvalidDicomError:
            sys.exit(f"{sys.argv[1]} is not a valid dicom file.")
        except Exception as e:
            sys.exit(e)

    # handle `python dcm_anon.py input_dir output_dir`
    if os.path.isdir(sys.argv[1]):
        if not os.path.isdir(sys.argv[2]):
            sys.exit(""" error: first input is folder, but second input is file""")
            sys.exit(usage)
        else:
            input_root_dir = sys.argv[1]
            output_root_dir = sys.argv[2]
            if not os.path.exists(output_root_dir):
                os.makedirs(output_root_dir)

            # walk dicom files
            for current_dir, dirs, filenames in os.walk(input_root_dir):
                # mkdir in output_root_dir
                for dir in dirs:
                    output_full_dir = os.path.join(current_dir, dir).replace(
                        input_root_dir, output_root_dir
                    )
                    if not os.path.exists(output_full_dir):
                        os.makedirs(output_full_dir)

                for filename in filenames:
                    full_filename = os.path.join(current_dir, filename)
                    output_full_filename = full_filename.replace(
                        input_root_dir, output_root_dir
                    )

                    try:
                        anonymize_and_save(
                            full_filename, output_full_filename, tags2anon
                        )
                    except pydicom.errors.InvalidDicomError:
                        # logging if not a valid dicom file, then process next file
                        sys.stdout(f"{full_filename} is not a valid dicom file.")
                    except Exception as e:
                        sys.exit(e)

    return 0


if __name__ == "__main__":
    sys.exit(main())
