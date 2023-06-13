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

    args = parser.parse_args()

    files = args.files
    prompt = args.mission
    llm = args.llm

    if args.llm != "openai":
        if not os.environ.get("HUGGINGFACEHUB_API_TOKEN"):
            raise ValueError(
                "The environment variable HUGGINGFACE_API_KEY is not set. "
                "You must have a HuggingFace account to use DocuSage with a custom LLM."
            )

    print(LOGO)
    print("Analyzing documents: ", files)
    if prompt:
        print("Mission: ", prompt)
    print("=" * 80)
    result = Mission(files, prompt, llm).write_report_with_sources()
    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
    print(result)
