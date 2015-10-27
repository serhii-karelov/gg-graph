import pytest


@pytest.fixture(scope='module')
def csv_file_path(tmpdir_factory):
    csv_data = "A,B,5\nB,C,4\nC,D,8\nD,C,8\nD,E,6\nA,D,5\nC,E,2\nE,B,3\nA,E,7\n"
    f = tmpdir_factory.mktemp('input_files').join('data.csv')
    f.write(csv_data)
    return str(f)
