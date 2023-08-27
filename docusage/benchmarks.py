import asyncio
from glob import glob
import os

from tqdm.asyncio import tqdm

from docusage.analyzer import Mission


def get_document_pairs():
    doc_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "tests", "docs"
    )
    ai_docs = glob(os.path.join(doc_dir, "ai", "*.pdf"))
    biosecurity_docs = glob(os.path.join(doc_dir, "biosecurity", "*.pdf"))

    min_len = min(len(ai_docs), len(biosecurity_docs), 5)

    for size in range(2, min_len + 1):
        for i in range(0, min_len - size + 1):
            combo1 = biosecurity_docs[i : i + size]
            combo2 = ai_docs[i : i + size]
            yield combo1, combo2


def check_if_ai(doc: str) -> bool:
    return (
        "artificial intelligence" in doc.lower() or "autonomous systems" in doc.lower()
    )


def check_if_biosecurity(doc: str) -> bool:
    return (
        "biosecurity" in doc.lower()
        or "global health" in doc.lower()
        or "bioeconomy" in doc.lower()
        or "gain of function research" in doc.lower()
        or "pathogen" in doc.lower()
    )


def check_hallucinations(doc: str, mission: str) -> bool:
    pass


async def reference_accuracy_benchmark(max_report_pairs=2):
    pbar = tqdm(
        total=max_report_pairs * 2,
        desc="Generating and testing reports",
        unit=" report",
    )
    metrics = {"Artificial intelligence": [0, 0], "Biosecurity": [0, 0]}

    for i, (biosecurity_docs, ai_docs) in enumerate(get_document_pairs()):
        if i > max_report_pairs:
            break
        for mission_type in ["Artificial intelligence", "Biosecurity"]:
            mission = await Mission.create(
                biosecurity_docs + ai_docs,
                mission_type,
                use_dynamic_section_headers=True,
            )
            report = await mission.write_report(inline_refs=True, length="tiny")
            val = (
                int(check_if_ai(report))
                if mission_type == "Artificial intelligence"
                else check_if_biosecurity(report)
            )
            if check_if_ai(report) and check_if_biosecurity(report):
                val = 0
            metrics[mission_type][val] += 1
            pbar.update(1)
    pbar.close()
    return metrics


async def reference_hallucination_benchmark(max_report_pairs=25):
    pbar = tqdm(
        total=max_report_pairs * 2,
        desc="Generating and testing reports",
        unit=" report",
    )
    metrics = {"Artificial intelligence": 0, "Biosecurity": 0}

    for i, (biosecurity_docs, ai_docs) in enumerate(get_document_pairs()):
        if i > max_report_pairs:
            break
        for mission_type in ["Artificial intelligence", "Biosecurity"]:
            if mission_type == "Artificial intelligence":
                docs = biosecurity_docs
            else:
                docs = ai_docs
            mission = await Mission.create(
                docs,
                mission_type,
                use_dynamic_section_headers=True,
            )
            report = await mission.write_report(inline_refs=True, length="tiny")
            int(check_hallucinations(report, mission_type))
            pbar.update(1)
    pbar.close()
    return metrics


async def async_main():
    metrics = await reference_accuracy_benchmark()
    print(metrics)


def main():
    asyncio.run(async_main())
