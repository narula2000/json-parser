import glob
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


class TestJsonChecker:
    TEST_DIR = "tests/json_checker"

    @pytest.mark.parametrize(
        "json_file",
        glob.glob(os.path.join(TEST_DIR, "pass*.json")),
        ids=lambda f: os.path.basename(f),
    )
    def test_pass_files(self, json_file):
        """All pass*.json files should exit with code 0"""
        with pytest.raises(SystemExit) as exc:
            main([json_file])

        assert exc.value.code == 0, f"Expected pass but failed: {json_file}"

    @pytest.mark.parametrize(
        "json_file",
        glob.glob(os.path.join(TEST_DIR, "fail*.json")),
        ids=lambda f: os.path.basename(f),
    )
    def test_fail_files(self, json_file):
        """All fail*.json files should exit with code 1"""
        if os.path.basename(json_file) == "fail18.json":
            pytest.xfail("Ignore failure: software validate json object depth up to 1,000,000 recursion limit")

        with pytest.raises(SystemExit) as exc:
            main([json_file])

        assert exc.value.code == 1, f"Expected fail but passed: {json_file}"
