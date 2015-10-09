import json


def main():
	with open('cyber_events.json', 'r') as json_file:
		a = json.loads(json_file)
	return a



if __name__ == '__main__':
	main()
