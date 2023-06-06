from typing import Iterable
from langchain.document_loaders import UnstructuredFileLoader
from langchain.indexes import VectorstoreIndexCreator

questions = [
    "Please provide a brief overview of {}.",
    "What are some key historical events or developments related to {}?",
    "Who are the key figures related to {}?",
    "What are the major organizations or entities involved in {}?",
    "What is the current state of affairs in relation to {}?",
    "What recent developments or events have occurred in {}?",
    "What are the primary challenges or issues associated with {}?",
    "What risks or threats are currently present in {}?",
    "What is the impact of these challenges or risks on the broader context of {}?",
    "What trends are emerging in relation to {}?",
    "What are possible future developments or scenarios in {}?",
    "What factors are contributing to the current situation and possible future trends in {}?",
    "What implications do these findings have for stakeholders in {}?",
    "What actions could be taken in response to the identified challenges and trends in {}?",
    "What opportunities exist in the current scenario of {}?",
]

section_headers = [
    "Executive Summary",
    "Historical Context",
    "Key Figures and Entities",
    "Organizational Landscape",
    "Current State of Affairs",
    "Recent Developments",
    "Challenges and Issues",
    "Risks and Threats",
    "Impact of Challenges and Risks",
    "Emerging Trends",
    "Forecast and Potential Scenarios",
    "Contributing Factors and Analysis",
    "Implications for Stakeholders",
    "Proposed Actions and Strategies",
    "Opportunities",
]


class Mission:
    def __init__(self, docs: Iterable[str], mission: str = "the topic"):
        loaders = [UnstructuredFileLoader(path) for path in docs]
        self.index = VectorstoreIndexCreator().from_loaders(loaders)
        self.mission = mission

    def write_report(self) -> str:
        report = f"## INTELLIGENCE REPORT\n\n"
        for i, question in enumerate(questions):
            report += f"#### {section_headers[i]}\n\n"
            report += self.index.query(question.format(self.mission))
            report += "\n\n"

        return report

    def write_report_with_sources(self) -> str:
        report = f"## INTELLIGENCE REPORT\n\n"
        for i, question in enumerate(questions):
            report += f"#### {section_headers[i]}\n\n"
            result = self.index.query_with_sources(question.format(self.mission))
            report += result["answer"]
            report += "\n\n"
            if result.get("sources"):
                if isinstance(result["sources"], str):
                    result["sources"] = [result["sources"]]
                report += "**Sources**\n\n"
                for source in result["sources"]:
                    report += f"- {source}\n"
                report += "\n"

        return report
