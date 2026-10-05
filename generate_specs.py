import json
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_json(filename):
    """
    Load a JSON configuration file.
    """
    path = BASE_DIR / filename

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------
# Load configuration files
# --------------------------------------------------

taxonomy = load_json("taxonomy.json")
skeletons = load_json("skeletons.json")
factors = load_json("factors.json")
constraints = load_json("document_constraints.json")


# --------------------------------------------------
# Build global document pool
# --------------------------------------------------

def get_all_document_types():
    """
    Flatten taxonomy into a list of:
    (category, document_type)

    Every document type therefore has equal probability
    when random.choice() is used.
    """

    document_pairs = []

    for category, document_types in taxonomy.items():
        for document_type in document_types:
            document_pairs.append(
                (category, document_type)
            )

    return document_pairs


DOCUMENT_PAIRS = get_all_document_types()


# --------------------------------------------------
# Configuration validation
# --------------------------------------------------

def validate_configs():
    """
    Validate consistency among taxonomy, skeletons,
    factors, and document constraints.
    """

    errors = []

    taxonomy_documents = {
        document_type
        for _, document_type in DOCUMENT_PAIRS
    }

    skeleton_documents = set(skeletons.keys())
    constraint_documents = set(constraints.keys())

    # Check missing skeletons
    for document_type in sorted(
        taxonomy_documents - skeleton_documents
    ):
        errors.append(
            f"Missing skeleton: {document_type}"
        )

    # Check missing constraints
    for document_type in sorted(
        taxonomy_documents - constraint_documents
    ):
        errors.append(
            f"Missing constraints: {document_type}"
        )

    # Check extra skeletons
    for document_type in sorted(
        skeleton_documents - taxonomy_documents
    ):
        errors.append(
            f"Skeleton exists but is not in taxonomy: "
            f"{document_type}"
        )

    # Check extra constraints
    for document_type in sorted(
        constraint_documents - taxonomy_documents
    ):
        errors.append(
            f"Constraints exist but document is not "
            f"in taxonomy: {document_type}"
        )

    # Check skeleton structure
    required_skeleton_keys = {
        "overall_description",
        "layout_structure",
        "image_text"
    }

    for document_type in taxonomy_documents:

        if document_type not in skeletons:
            continue

        skeleton = skeletons[document_type]

        missing_keys = (
            required_skeleton_keys
            - set(skeleton.keys())
        )

        for key in sorted(missing_keys):
            errors.append(
                f"{document_type}: "
                f"missing skeleton key '{key}'"
            )

        if "image_text" in skeleton:

            image_text = skeleton["image_text"]

            if not isinstance(image_text, list):
                errors.append(
                    f"{document_type}: "
                    f"image_text must be a list"
                )

            elif len(image_text) < 6:
                errors.append(
                    f"{document_type}: "
                    f"image_text has fewer than 6 fields"
                )

    # Check constraints against factors.json
    for document_type in taxonomy_documents:

        if document_type not in constraints:
            continue

        document_constraints = constraints[
            document_type
        ]

        for factor_name, allowed_values in (
            document_constraints.items()
        ):

            if factor_name not in factors:
                errors.append(
                    f"{document_type}: "
                    f"unknown factor '{factor_name}'"
                )
                continue

            valid_values = set(
                factors[factor_name]
            )

            for value in allowed_values:
                if value not in valid_values:
                    errors.append(
                        f"{document_type}: "
                        f"invalid value '{value}' "
                        f"for factor '{factor_name}'"
                    )

    if errors:

        print("\nConfiguration validation failed:\n")

        for error in errors:
            print(f"- {error}")

        raise ValueError(
            f"Found {len(errors)} "
            f"configuration error(s)."
        )

    print(
        f"Configuration validation passed: "
        f"{len(DOCUMENT_PAIRS)} document types."
    )


# --------------------------------------------------
# Field sampling
# --------------------------------------------------

def sample_image_text(fields):
    """
    Randomly select 70%-100% of image-text fields.

    At least 6 fields are preserved to keep
    the resulting document text-rich.
    """

    min_fields = max(
        6,
        int(len(fields) * 0.7)
    )

    max_fields = len(fields)

    number_to_select = random.randint(
        min_fields,
        max_fields
    )

    selected = random.sample(
        fields,
        number_to_select
    )

    return selected


# --------------------------------------------------
# Generate one spec
# --------------------------------------------------

def generate_spec():
    """
    Generate one structured document specification.

    All document types are sampled with equal probability.
    """

    # 1. Select document type globally.
    category, document_type = random.choice(
        DOCUMENT_PAIRS
    )

    # 2. Read its skeleton.
    skeleton = skeletons[
        document_type
    ]

    # 3. Read its allowed factor pools.
    document_constraints = constraints[
        document_type
    ]

    # 4. Sample image-text fields.
    selected_fields = sample_image_text(
        skeleton["image_text"]
    )

    # 5. Build structured specification.
    spec = {
        "category": category,

        "document_type": document_type,

        "overall_description":
            skeleton["overall_description"],

        "layout_structure":
            skeleton["layout_structure"],

        "image_text":
            selected_fields,

        # Global factor
        "language":
            random.choice(
                factors["language"]
            ),

        # Document-specific factors
        "orientation":
            random.choice(
                document_constraints[
                    "orientation"
                ]
            ),

        "text_density":
            random.choice(
                document_constraints[
                    "text_density"
                ]
            ),

        "capture_style":
            random.choice(
                document_constraints[
                    "capture_style"
                ]
            ),

        "layout_style":
            random.choice(
                document_constraints[
                    "layout_style"
                ]
            ),

        "visual_condition":
            random.choice(
                document_constraints[
                    "visual_condition"
                ]
            ),

        "document_theme":
            random.choice(
                document_constraints[
                    "document_theme"
                ]
            ),

        "background":
            random.choice(
                document_constraints[
                    "background"
                ]
            )
    }

    return spec


# --------------------------------------------------
# Generate multiple specs
# --------------------------------------------------

def generate_specs(count):
    """
    Generate multiple independent specs.
    """

    if count < 1:
        raise ValueError(
            "count must be at least 1."
        )

    return [
        generate_spec()
        for _ in range(count)
    ]


# --------------------------------------------------
# Local test
# --------------------------------------------------

if __name__ == "__main__":

    validate_configs()

    spec = generate_spec()

    print(
        json.dumps(
            spec,
            ensure_ascii=False,
            indent=2
        )
    )