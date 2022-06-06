import json 

var = {
	"projects": [
		{
		"name": "A",
		"hours": "0",
		"mins": "0",
		"secs": "0"
		},
		{
		"name": "B",
		"hours": "1",
		"mins": "1",
		"secs": "1"
					}
				]
		}

def write_json(data, filename):
	with open(filename, "w") as file:
		json.dump(data, file, indent=2)

def read_json(filename):
	with open(filename) as file:
		data = json.load(file)
	return data


def main():
	write_json(var, "test.json")
	data = read_json("test.json")
	for project in data["projects"]:
		print(project["name"])


if __name__ == "__main__":
	main()