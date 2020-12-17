from datetime import datetime
from lzma import LZMAFile
from pathlib import Path

from bigxml import Parser, xml_handle_element, xml_handle_text


def test_wikipedia_export():
    class Revision:
        def __init__(self):
            self.author = None
            self.date = None

        @xml_handle_text("contributor", "username")
        def handle_author(self, node):
            self.author = node.text

        @xml_handle_text("timestamp")
        def handle_date(self, node):
            self.date = datetime.strptime(node.text, "%Y-%m-%dT%H:%M:%SZ")

    @xml_handle_element("mediawiki", "page", "revision")
    def handler(node):
        revision = Revision()
        node.return_from(revision)
        yield revision

    with LZMAFile(Path(__file__).parent / "wikipedia_python_export.xml.xz") as stream:
        items = list(Parser(stream).iter_from(handler))
        assert len(items) == 1000
        revision = items[-1]
        assert isinstance(revision, Revision)
        assert revision.author == "Lulu of the Lotus-Eaters"
        assert revision.date.year == 2006
        assert revision.date.month == 4
        assert revision.date.day == 14
        assert revision.date.hour == 15
        assert revision.date.minute == 58
