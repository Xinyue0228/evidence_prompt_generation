import argparse
import time
from datetime import datetime
from pathlib import Path

from generate_specs import (
    generate_spec,
    validate_configs
)

from expand_prompt import expand_prompt


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def generate_one():
    """
    Generate one final prompt only.
    Language is controlled by spec["language"].
    """

    spec = generate_spec()

    final_prompt = expand_prompt(spec).strip()

    return {
        "language": spec["language"],
        "document_type": spec["document_type"],
        "prompt": final_prompt
    }


def save_prompts_txt(prompts, output_path):
    """
    Save prompts to a plain text file.
    Only prompt text is saved.
    One prompt block per entry.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_path, "w", encoding="utf-8") as f:
        for i, prompt in enumerate(prompts, start=1):
            f.write(prompt.strip())
            if i < len(prompts):
                f.write("\n\n")


def run_single(output=None):
    """
    Generate one prompt and print it.
    """

    print("\nGenerating one prompt...\n")

    record = generate_one()

    print("Document type:", record["document_type"])
    print("Language:", record["language"])
    print("\nPrompt:\n")
    print(record["prompt"])

    if output:
        output_path = OUTPUT_DIR / output
        save_prompts_txt([record["prompt"]], output_path)
        print(f"\nSaved to: {output_path}")


def run_batch(count, output=None, sleep_seconds=0):
    """
    Generate multiple prompts and save only prompt text to .txt.
    """

    if count < 1:
        raise ValueError("count must be at least 1.")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if output is None:
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        output = f"prompts_{count}_{timestamp}.txt"

    output_path = OUTPUT_DIR / output

    prompts = []

    success_count = 0
    failure_count = 0

    print(
        f"\nStarting batch generation: "
        f"{count} prompts\n"
    )

    for index in range(count):

        print(f"[{index + 1}/{count}] ", end="")

        try:
            record = generate_one()

            prompts.append(record["prompt"])
            success_count += 1

            print(
                f"OK - "
                f"{record['document_type']} "
                f"({record['language']})"
            )

        except Exception as error:
            failure_count += 1
            print(f"FAILED - {error}")

        # save progress every step
        save_prompts_txt(prompts, output_path)

        if sleep_seconds > 0 and index < count - 1:
            time.sleep(sleep_seconds)

    print("\nBatch finished.")
    print(f"Success: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Saved to: {output_path}")


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Generate final image-generation prompts "
            "for Evidence Records."
        )
    )

    subparsers = parser.add_subparsers(
        dest="mode",
        required=True
    )

    single_parser = subparsers.add_parser(
        "single",
        help="Generate one prompt."
    )
    single_parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional output TXT filename."
    )

    batch_parser = subparsers.add_parser(
        "batch",
        help="Generate prompts in batch."
    )
    batch_parser.add_argument(
        "--count",
        type=int,
        required=True,
        help="Number of prompts to generate."
    )
    batch_parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output TXT filename."
    )
    batch_parser.add_argument(
        "--sleep",
        type=float,
        default=0,
        help="Optional delay between API calls in seconds."
    )

    args = parser.parse_args()

    validate_configs()

    if args.mode == "single":
        run_single(output=args.output)

    elif args.mode == "batch":
        run_batch(
            count=args.count,
            output=args.output,
            sleep_seconds=args.sleep
        )


if __name__ == "__main__":
    main()