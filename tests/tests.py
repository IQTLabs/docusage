from glob import glob
import pytest
import os
from docusage.analyzer import Mission


def get_file(name: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", name)


### CODE AND STRUCTURE TESTS ###
@pytest.mark.asyncio
async def test_initialization():
    """
    Test if the Mission object initializes without error.
    """
    mission = await Mission.create(docs=[get_file("IF11333.pdf")])
    assert mission is not None


### STATISTICAL TESTS ###
@pytest.mark.asyncio
async def test_correct_mission_discovery():
    """
    Test if a suitable mission/subject is discovered.
    """
    mission = await Mission.create(docs=[get_file("IF11333.pdf")])
    discovered_mission = mission.mission
    assert len(discovered_mission.split()) <= 6
    assert not discovered_mission.endswith(".")
    assert (
        "deepfake" in discovered_mission.lower()
        or "deep fake" in discovered_mission.lower()
    )


@pytest.mark.asyncio
async def test_irrelevant_documents_should_create_not_create_a_mission():
    """
    Test if irrelevant documents are not used to create a mission.
    """
    try:
        await Mission.create(docs=[get_file("Nonsensical.txt")])
    except ValueError:
        assert True
    else:
        assert False


@pytest.mark.asyncio
async def test_dynamic_section_headers():
    """
    Test if dynamic section headers are created.
    """
    mission = await Mission.create(
        docs=[get_file("IF11333.pdf")],
        use_dynamic_section_headers=True,
    )
    assert len(mission.section_headers) > 0
    assert len(mission.questions) > 0
    assert len(mission.section_headers) == len(mission.questions)
    assert (
        len(
            [
                header
                for header in mission.section_headers
                if "deep fake" in header.lower() or "deepfake" in header.lower()
            ]
        )
        > 0
    )


@pytest.mark.asyncio
async def test_references():
    """
    Test if DocuSage references the correct documents.
    """
    mission = await Mission.create(
        docs=[get_file("IF11333.pdf"), get_file("R47114.pdf")],
        use_dynamic_section_headers=True,
        mission="Gain of Function Research",
    )
    assert len(mission.section_headers) > 0
    assert len(mission.questions) > 0
    assert len(mission.section_headers) == len(mission.questions)

    report = await mission.write_report(inline_refs=True, length="tiny")
    report = report.lower()
    assert "deep fake" not in report
    assert "deepfake" not in report
    assert "if11333" not in report
    assert "gain of function" in report
    assert "references" in report
