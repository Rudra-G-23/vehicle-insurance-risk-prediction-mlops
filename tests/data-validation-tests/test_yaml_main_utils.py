from src.utils.main_utils import read_yaml_file, write_yaml_file

# sample data
data = {
    "name": "Rudra",
    "role": "Data Scientist",
    "skills": ["Python", "ML", "SQL"]
}

file_path = ".venv/test.yaml"

# write yaml
write_yaml_file(file_path=file_path, content=data)

print("YAML file written successfully")

# read yaml
read_data = read_yaml_file(file_path=file_path)

print("YAML file read successfully")
print(read_data)