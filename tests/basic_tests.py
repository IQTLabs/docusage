from glob import glob
import os
import pytest
from docusage.analyzer import Mission, section_headers

script_dir = os.path.dirname(os.path.abspath(__file__))

# Sample documents for the tests from the Congressional Research Service
sample_docs = [doc for doc in glob(os.path.join(script_dir, "docs", "*.pdf"))]

def test_initialization():
    """
    Test if the Mission object initializes without error.
    """
    mission = Mission(docs=sample_docs)
    assert mission is not None


def test_mission_discovery():
    """
    Test if a suitable mission/subject is discovered.
    """
    mission = Mission(docs=sample_docs)
    discovered_mission = mission._find_the_mission()
    assert len(discovered_mission.split()) <= 6
    assert not discovered_mission.endswith(".")


def test_report_writing():
    """
    Test the output format of the write_report method.
    """
    mission = Mission(docs=sample_docs)
    report = mission.write_report()
    assert "INTELLIGENCE REPORT:" in report
    for header in section_headers:
        assert header in report


def test_report_with_sources():
    """
    Test the output format and the presence of references in the write_report_with_sources method.
    """
    mission = Mission(docs=sample_docs)
    report = mission.write_report_with_sources()
    assert "INTELLIGENCE REPORT:" in report
    for header in section_headers:
        assert header in report
    assert "**References**" in report