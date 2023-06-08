from typing import Iterable
from pathlib import Path
from langchain.document_loaders import UnstructuredFileLoader
from langchain.indexes import VectorstoreIndexCreator

questions = [
    "Provide a comprehensive executive summary written for an intelligence report covering the main aspects of {}.",
    "Detail the current landscape of {}, identifying key actors and their roles. Describe the interaction between these key actors. Answer comprehensively.",
    "What are the significant recent developments in {}? Analyze their impact on the overall context.",
    "Identify and detail all potential risks, challenges, and threats facing {}? Answer comprehensively.",
    "What are the future projections for {} over the next 5-10 years? Answer comprehensively.",
    "Based on the analysis, what recommendations and opportunities can be made for stakeholders in {}? Answer comprehensively.",
]

section_headers = [
    "Executive Summary",
    "Current Landscape and Key Actors",
    "Recent Developments and Their Impact",
    "Potential Risks and Challenges",
    "Future Projections and Emerging Trends",
    "Recommendations and Opportunities",
]


class Mission:
    def __init__(
        self,
        docs: Iterable[str],
        mission: str = None,
    ):
        loaders = [UnstructuredFileLoader(path) for path in docs]
        self.index = VectorstoreIndexCreator().from_loaders(loaders)
        if not mission:
            mission = self._find_the_mission()
        self.mission = mission

    def _find_the_mission(self) -> str:
        mission = self.index.query(
            "What is a identified subject of interest with intelligence value "
            "to a Western government that is found in these documents? Write the"
            "answer in six words or less."
        )
        if mission.endswith("."):
            mission = mission[:-1]
        return mission

    def write_report(self) -> str:
        report = "INTELLIGENCE REPORT: {}\n\n".format(self.mission)
        for i, question in enumerate(questions):
            report += f"### {section_headers[i]}\n\n"
            report += self.index.query(question.format(self.mission))
            report += "\n\n"

        return report

    def write_report_with_sources(self) -> str:
        report = "INTELLIGENCE REPORT: {}\n\n".format(self.mission)
        for i, question in enumerate(questions):
            report += f"### {section_headers[i]}\n\n"
            result = self.index.query_with_sources(question.format(self.mission))
            report += result["answer"]
            report += "\n\n"
            if result.get("sources"):
                if isinstance(result["sources"], str):
                    result["sources"] = [result["sources"]]
                report += "**References**\n\n"
                for source in result["sources"]:
                    report += f"- {Path(source).name}\n"
                report += "\n"

        return report
