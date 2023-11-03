import os
import shutil


def test_command_line_less_than_3_args():
    command = "python dcm_anon.py"
    r = os.system(command)
    assert r == 1


def test_command_line_input_not_exist():
    command = "python dcm_anon.py non-exist-file.dcm output.dcm"
    r = os.system(command)
    assert r == 1


def test_command_line_input_file_but_output_folder():
    command = "python dcm_anon.py tests/CT/CT_small.dcm tests"
    r = os.system(command)
    assert r == 1


def test_command_line_input_dcmfile_output_path_to_dcmfile():
    command = "python dcm_anon.py tests/CT/CT_small.dcm tests/temp/test.dcm"
    r = os.system(command)
    assert r == 0


def test_command_line_input_folder_output_folder():
    command = "python dcm_anon.py tests/CT tests/temp"
    r = os.system(command)
    assert r == 0


def test_remove_temp_dir():
    if os.path.exists("tests/temp"):
        shutil.rmtree("tests/temp")
        assert 0 == 0
