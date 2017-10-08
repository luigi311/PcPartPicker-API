# PcPartPicker-API

Python3 API for getting part information from [PcPartPicker](https://uk.pcpartpicker.com)

Examples:

- Save all cpu data to `.json` file
	```python
	from PcPartPicker import PPP_API
	import json

	cpu_info = PPP_API.get_part("cpu")

	with open("cpu.json", "w") as outfile:
	    json.dump(cpu_info, outfile)
	```
