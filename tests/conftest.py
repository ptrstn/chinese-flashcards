import pathlib

SKIP_DOWNLOAD_TESTS = False
UNIHAN_TEST_PATH = pathlib.Path('test_data/unihan')


def clear_unihan_test_files():
    test_path = UNIHAN_TEST_PATH
    for path in reversed(list(test_path.glob("**/*"))):
        path.unlink()
    test_path.rmdir()
    assert not test_path.exists()
