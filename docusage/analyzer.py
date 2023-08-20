from typing import Iterable, List, Dict
from paperqa import Docs
from langchain.document_loaders import UnstructuredFileLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI, HuggingFaceHub


class Mission:
    questions: List[str] = [
        "Provide a executive summary written for an intelligence report covering the main aspects of {}.",
        "Detail the current landscape of {}, identifying key actors and their roles. Describe the interaction between these key actors.",
        "What are the significant recent developments in {}? Analyze their impact on the overall context.",
        "Identify and detail all potential risks, challenges, and threats facing {}?",
        "What are the future projections for {} over the next 5-10 years?",
        "Based on the analysis, what recommendations and opportunities can be made for for the United States national security establishment to address {}?",
    ]

    section_headers: List[str] = [
        "Executive Summary",
        "Current Landscape and Key Actors",
        "Recent Developments and Their Impact",
        "Potential Risks and Challenges",
        "Future Projections and Emerging Trends",
        "Recommendations and Opportunities",
    ]

    length_prompts: Dict[str, str] = {
        "tiny": "no more than one sentence",
        "small": "no more than one paragraph",
        "medium": "two paragraphs",
        "large": "three to five paragraphs",
        "xlarge": "five paragraphs or more",
    }

    def __init__(
        self,
        docs: Iterable[str],
        mission: str = None,
        llm: str = "openai",
    ):
        if llm == "openai":
            llm = OpenAI(max_tokens=500, temperature=0)
        else:
            llm = HuggingFaceHub(
                repo_id=llm, model_kwargs={"temperature": 0, "max_length": 500}
            )

        self.index = Docs()
        for doc in docs:
            self.index.add(doc)

        if not mission:
            self.mission = self._find_the_mission()
        else:
            self.mission = mission

    def _find_the_mission(self) -> str:
        response = self.index.query(
            "What is a identified subject of interest with intelligence value "
            "to a Western government that is found in these documents? Respond in six words or less.",
            length_prompt="strictly six words or less",
        )
        mission = response.answer
        if mission.endswith("."):
            mission = mission[:-1]
        mission = mission.split("(")[0].strip()
        if "I cannot answer" in mission or "I can't answer" in mission:
            raise ValueError("No overall mission purpose was found in the documents.")
        return mission

    def write_report(
        self,
        inline_context: bool = False,
        inline_refs: bool = False,
        length: str = "medium",
    ) -> str:
        report = "INTELLIGENCE REPORT: {}\n\n".format(self.mission)
        for i, question in enumerate(self.questions):
            response = self.index.query(
                question.format(self.mission), length_prompt=self.length_prompts[length]
            )
            if (
                "I cannot answer" in response.answer
                or "I can't answer" in response.answer
            ):
                report += "\n\n"
                continue
            report += f"### {self.section_headers[i]}\n\n"
            report += response.answer
            report += "\n\n"
            if inline_refs:
                report += "**References**\n\n"
                report += response.references
                report += "\n\n"
            if inline_context:
                report += "**Context**\n\n"
                for context in response.contexts:
                    report += f"* {context.text.text} (Score: {context.score})\n"
                report += "\n\n"
            report += "\n\n"

        return report
