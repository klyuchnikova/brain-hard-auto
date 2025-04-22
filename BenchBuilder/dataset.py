import orjson
import pandas as pd
from typing import List, Dict, Any
import argparse
import os
from label import _get_uid, _get_prompt
from category import Category

def load_and_process_dataset(dataset_path: str) -> List[Dict[str, Any]]:
    """
    Loads a dataset from the given path and processes it into a JSON array with keys: id, instruction.
    Instruction is a list of conversation dictionaries.

    Args:
        dataset_path (str): Path to the dataset file.

    Returns:
        List[Dict[str, Any]]: List of dictionaries with keys 'id' and 'instruction'.
    """
    print("Loading input data...")
    with open(dataset_path, "rb") as f:
        data = orjson.loads(f.read())
    input_data = pd.DataFrame(data)

    input_data["uid"] = input_data.apply(_get_uid, axis=1)
    assert len(input_data) == len(input_data.uid.unique())
    print(f"{len(input_data)}# of input data rows just loaded")
    input_data["instruction"] = input_data["conversation_a"].map(lambda conv: _get_prompt(conv))
    input_data["instruction"] = input_data.instruction.map(lambda x: x[:12500])

    category = Category.create_category()
    print(
        f"Following categories will be labeled:\n{category.name_tag}"
    )

    processed_data = []
    for _, row in input_data.iterrows():
        processed_entry = {
            "id": row.get("uid"),
            "instruction": category.pre_process(row.get("instruction", []))
        }
        processed_data.append(processed_entry)
    return processed_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, required=True, help="Path to the dataset file")
    args = parser.parse_args()

    processed_dataset = load_and_process_dataset(args.dataset_path)

    output_path = os.path.splitext(args.dataset_path)[0] + "_processed.json"
    with open(output_path, "wb") as f:
        f.write(orjson.dumps(processed_dataset, option=orjson.OPT_INDENT_2))

    print(f"Processed dataset saved to {output_path}")
