import os
import argparse

from docusage.analyzer import Mission

LOGO = r"""                                               
     ____                  _____                
    |    \  ___  ___  _ _ |   __| ___  ___  ___ 
    |  |  || . ||  _|| | ||__   || .'|| . || -_|
    |____/ |___||___||___||_____||__,||_  ||___|
                                      |___|     
    """


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError(
            "The environment variable OPENAI_API_KEY is not set. You must have a paid OpenAI account to use DocuSage."
        )

    parser = argparse.ArgumentParser(
        description=f"{LOGO}\nGenerate an intelligence report from a set of documents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "files",
        metavar="FILES",
        type=str,
        nargs="+",
        help="a list of files to be analyzed",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=False,
        help="an optional output file path",
    )
    parser.add_argument(
        "--mission", "-m", type=str, required=False, help="an optional mission prompt"
    )
    parser.add_argument(
        "--llm",
        "-l",
        type=str,
        required=False,
        default="openai",
        help="the language model to use",
    )
    parser.add_argument(
        "--no-inline-references",
        "-r",
        action="store_false",
        default=True,
        help="don't include references in the report",
    )
    parser.add_argument(
        "--no-inline-context",
        "-c",
        action="store_false",
        default=True,
        help="don't include context from the source material in the report",
    )
    parser.add_argument(
        "--length",
        "-n",
        type=str,
        required=False,
        default="medium",
        choices=["tiny", "small", "medium", "large", "xlarge"],
        help="the length of the report",
    )

    args = parser.parse_args()

    if args.llm != "openai":
        if not os.environ.get("HUGGINGFACEHUB_API_TOKEN"):
            raise ValueError(
                "The environment variable HUGGINGFACE_API_KEY is not set. "
                "You must have a HuggingFace account to use DocuSage with a custom LLM."
            )

    print(LOGO)
    print("Analyzing documents:", args.files)
    mission = Mission(args.files, args.mission, args.llm)
    print("Mission:", mission.mission)
    print("Report length:", args.length)
    args.no_inline_context and print("Including context in report.")
    args.no_inline_references and print("Including references in report.")
    print("=" * 80)
    result = mission.write_report(
        args.no_inline_context, args.no_inline_references, args.length
    )
    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
    print(result)
