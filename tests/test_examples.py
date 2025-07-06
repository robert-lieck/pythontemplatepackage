import pathlib

from . import TestFolder


class TestExamples(TestFolder):
    __test__ = True

    @classmethod
    def dir(cls):
        return pathlib.Path(__file__).parent.resolve() / ".." / "examples"


class TestNotebooks(TestFolder):
    __test__ = True

    @classmethod
    def dir(cls):
        return pathlib.Path(__file__).parent.resolve() / "notebooks"
