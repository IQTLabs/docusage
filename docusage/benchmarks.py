from argparse import ArgumentParser
import asyncio
from glob import glob
import os
from logging import getLogger

from tqdm.asyncio import tqdm

from docusage.analyzer import Mission

logger = getLogger(__name__)


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
    return any(
        keyword in doc.lower()
        for keyword in [
            "biosecurity",
            "global health",
            "bioeconomy",
            "gain of function research",
            "pathogen",
        ]
    )


def check_hallucinations(doc: str, mission: str) -> bool:
    pass


async def reference_accuracy_benchmark(
    max_report_pairs: int = 2, report_path: str = None
):
    pbar = tqdm(
        total=max_report_pairs * 2,
        desc="Generating and testing reports",
        unit=" report",
    )
    metrics = {"Artificial intelligence": [0, 0], "Biosecurity": [0, 0]}

    for i, (biosecurity_docs, ai_docs) in enumerate(get_document_pairs()):
        if i >= max_report_pairs:
            break
        for mission_type in ["Artificial intelligence", "Biosecurity"]:
            pbar.update(1)
            try:
                mission = await Mission.create(
                    biosecurity_docs + ai_docs,
                    mission_type,
                    use_dynamic_section_headers=True,
                    ignore_failures=True,
                )
            except ValueError as e:
                logger.error(f"{i}_{mission_type}.txt: could not be generated: {e}")
                continue
            report = await mission.write_report(inline_refs=True, length="tiny")
            if report_path:
                if not os.path.exists(report_path):
                    os.makedirs(report_path)
                with open(
                    os.path.join(report_path, f"{i}_{mission_type}.txt"), "w"
                ) as f:
                    f.write(report)
            val = (
                int(check_if_ai(report))
                if mission_type == "Artificial intelligence"
                else check_if_biosecurity(report)
            )
            if val == 1:
                logger.info(f"{i}_{mission_type}.txt: is {mission_type}")
            elif val == 0:
                logger.info(f"{i}_{mission_type}.txt: is not {mission_type}")

            if check_if_ai(report) and check_if_biosecurity(report):
                val = 0
                logger.info(f"{i}_{mission_type}.txt: is both AI and Biosecurity")
            metrics[mission_type][val] += 1
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
    parser = ArgumentParser(description="DocuSage benchmarking tool")
    parser.add_argument(
        "--max-report-pairs",
        "-n",
        type=int,
        required=False,
        default=2,
        help="the number of report pairs to generate",
    )
    parser.add_argument(
        "--report-path",
        "-o",
        type=str,
        required=False,
        default=None,
        help="the path to save the reports",
    )
    args = parser.parse_args()
    metrics = await reference_accuracy_benchmark(
        args.max_report_pairs, args.report_path
    )
    print(metrics)


def main():
    asyncio.run(async_main())
