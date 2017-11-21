from PcPartPicker import PPP_API
import json


components = ["motherboard","memory"]
for comp in components:
    cpu_info = PPP_API.get_part(comp)

    with open(comp+".json", "w") as outfile:
        json.dump(cpu_info, outfile)