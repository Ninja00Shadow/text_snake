import pathlib

BASE = pathlib.Path(__file__).parent
file_path = BASE / "defaults.txt"

def read_defaults():
    """Read the default values from the file."""
    defaults = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                defaults[key] = int(value)
    except FileNotFoundError:
        defaults = {
            "speed": 20,
            "length": 3
        }
        write_defaults(defaults)
    return defaults

def write_defaults(defaults:dict):
    """Write the default values to the file."""
    with open(file_path, "w") as file:
        for key, value in defaults.items():
            file.write(f"{key}={value}\n")

if __name__ == "__main__":
    print(read_defaults())