import os

import pytest

from main import main


class TestStep1:
    TEST_DIR = "tests/step1"

    def test_valid(self):
        """Testing json parser step1 valid command"""
        test_args = [
            os.path.join(
                self.TEST_DIR,
                "valid.json",
            )
        ]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(test_args)
        assert pytest_wrapped_e.value.code == 0

    def test_invalid(self):
        """Testing json parser step1 invalid command"""
        test_args = [
            os.path.join(
                self.TEST_DIR,
                "invalid.json",
            )
        ]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(test_args)
        assert pytest_wrapped_e.value.code == 1


class TestStep2:
    TEST_DIR = "tests/step2"

    def test_valid_1(self):
        """Testing json parser step1 valid command"""
        test_args = [
            os.path.join(
                self.TEST_DIR,
                "valid.json",
            )
        ]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(test_args)
        assert pytest_wrapped_e.value.code == 0

    def test_valid_2(self):
        """Testing json parser step1 valid command"""
        test_args = [
            os.path.join(
                self.TEST_DIR,
                "valid2.json",
            )
        ]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(test_args)
        assert pytest_wrapped_e.value.code == 0

    def test_invalid_1(self):
        """Testing json parser step1 invalid command"""
        test_args = [
            os.path.join(
                self.TEST_DIR,
                "invalid.json",
            )
        ]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(test_args)
        assert pytest_wrapped_e.value.code == 1

    def test_invalid_2(self):
        """Testing json parser step1 invalid command"""
        test_args = [
            os.path.join(
                self.TEST_DIR,
                "invalid2.json",
            )
        ]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(test_args)
        assert pytest_wrapped_e.value.code == 1


class TestStep3:
    TEST_DIR = "tests/step3"

    def test_valid(self):
        """Testing json parser step1 valid command"""
        test_args = [
            os.path.join(
                self.TEST_DIR,
                "valid.json",
            )
        ]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(test_args)
        assert pytest_wrapped_e.value.code == 0

    def test_invalid(self):
        """Testing json parser step1 invalid command"""
        test_args = [
            os.path.join(
                self.TEST_DIR,
                "invalid.json",
            )
        ]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(test_args)
        assert pytest_wrapped_e.value.code == 1


@pytest.mark.skip(reason="Not part of the scope")
class TestStep4:
    TEST_DIR = "tests/step4"

    def test_valid_1(self):
        """Testing json parser step1 valid command"""
        test_args = [
            os.path.join(
                self.TEST_DIR,
                "valid.json",
            )
        ]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(test_args)
        assert pytest_wrapped_e.value.code == 0

    def test_valid_2(self):
        """Testing json parser step1 valid command"""
        test_args = [
            os.path.join(
                self.TEST_DIR,
                "valid2.json",
            )
        ]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(test_args)
        assert pytest_wrapped_e.value.code == 0

    def test_invalid(self):
        """Testing json parser step1 invalid command"""
        test_args = [
            os.path.join(
                self.TEST_DIR,
                "invalid.json",
            )
        ]
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main(test_args)
        assert pytest_wrapped_e.value.code == 1
