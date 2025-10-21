import csv
import os
import folder_paths


class SimpleCSVParser:
    """
    A ComfyUI custom node for parsing CSV files with positive and negative prompts.
    Supports both selecting from input folder and manual file path entry.
    """

    @classmethod
    def INPUT_TYPES(cls):
        # Get CSV files from input directory for dropdown
        input_dir = folder_paths.get_input_directory()
        try:
            files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
        except:
            files = []

        if not files:
            files = [""]

        return {
            "required": {
                "csv_from_folder": (sorted(files),),
                "csv_custom_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
                "index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10000,
                    "step": 1,
                    "display": "number"
                }),
                "use_negative_prompt": ("BOOLEAN", {
                    "default": True,
                    "label_on": "enabled",
                    "label_off": "disabled"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt", "total_rows", "total_rows_string")
    FUNCTION = "parse_csv"
    CATEGORY = "utils"

    def parse_csv(self, csv_from_folder, csv_custom_path, index, use_negative_prompt):
        """
        Parse CSV file and return prompts based on index.

        Args:
            csv_from_folder: File name from the input folder dropdown
            csv_custom_path: Custom file path entered manually
            index: Row index to read (0-based)
            use_negative_prompt: Whether to use the negative prompt column

        Returns:
            tuple: (positive_prompt, negative_prompt, total_rows, total_rows_text)
        """
        # Auto-detect which input to use
        # Priority: custom_path (if provided) > from_folder
        csv_custom_path_stripped = csv_custom_path.strip() if csv_custom_path else ""
        csv_from_folder_stripped = csv_from_folder.strip() if csv_from_folder else ""

        if csv_custom_path_stripped != "":
            # Use custom path
            csv_path = os.path.expanduser(csv_custom_path_stripped)
        elif csv_from_folder_stripped != "":
            # Use file from input folder
            input_dir = folder_paths.get_input_directory()
            csv_path = os.path.join(input_dir, csv_from_folder_stripped)
        else:
            return ("Error: Please select a CSV file from the dropdown OR enter a custom file path", "", 0, "0")

        # Check if file exists
        if not os.path.exists(csv_path):
            return (f"Error: CSV file not found at {csv_path}", "", 0, "0")

        try:
            # Read the CSV file
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)

                # Remove header if present (optional - assumes first row might be header)
                # You can modify this behavior if needed
                if len(rows) > 0 and rows[0][0].lower() in ['positive', 'positive_prompt', 'prompt']:
                    rows = rows[1:]  # Skip header row

                total_rows = len(rows)

                # Check if index is valid
                if index >= total_rows:
                    return (
                        f"Error: Index {index} out of range. Total rows: {total_rows}",
                        "",
                        total_rows,
                        str(total_rows)
                    )

                # Get the row at the specified index
                row = rows[index]

                # Extract positive prompt (first column)
                positive_prompt = row[0].strip() if len(row) > 0 else ""

                # Extract negative prompt (second column) if enabled
                negative_prompt = ""
                if use_negative_prompt and len(row) > 1:
                    negative_prompt = row[1].strip()

                return (positive_prompt, negative_prompt, total_rows, str(total_rows))

        except Exception as e:
            return (f"Error reading CSV: {str(e)}", "", 0, "0")


# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "SimpleCSVParser": SimpleCSVParser
}

# Display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleCSVParser": "Simple CSV Parser"
}
