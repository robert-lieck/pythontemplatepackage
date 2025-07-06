#  Copyright (c) 2022 Robert Lieck.
from unittest import TestCase

import os
import importlib.util


class TestFolder(TestCase):
    __test__ = False
    cwd = None

    @classmethod
    def dir(cls):
        raise NotImplementedError

    def setUp(self) -> None:
        self.cwd = os.getcwd()
        assert os.path.isdir(self.dir()), f"directory '{self.dir()}' does not exist"
        os.chdir(self.dir())

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        self.cwd = None

    def test_examples(self):
        """Run all the examples from the documentation."""
        for dir_path, dir_names, file_names in os.walk("."):
            for file in file_names:
                full_path = os.path.join(dir_path, file)
                if not file.endswith(".py"):
                    continue
                print(f"loading: {file}")
                # sourcing directly hides problematic lines in error traces
                # exec(open(os.path.join(dir_path, file)).read())
                # import as module instead
                spec = importlib.util.spec_from_file_location("", full_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
