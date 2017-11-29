from PcPartPicker import PPP_API, PPP_CPU
import json
sockets={"AM1":27, "AM3":3 ,"AM3+":4,"AM3/AM2+":6,
         "AM4":33, "BGA413":8, "BGA559":10,
         "BGA1023":25, "C32":32, "FM1":20,
         "FM2":23, "FM2+":26, "G34":31, "LGA771":12,
         "LGA775":13, "LGA1150":24, "LGA1151":30,
         "LGA1155":14, "LGA1156":15, "LGA1356":37,
         "LGA1366":16, "LGA2011":21, "LGA2011-3":28,
         "LGA2066":35, "PGA988":18, "TR4":36 }

components = ["motherboard","memory"]
print("Working on")
for comp in components:
    print(comp)
    comp_info = PPP_API.get_part(comp)

    with open(comp+".json", "w") as outfile:
        json.dump(comp_info, outfile)

print("Cpus")
for key,value in sockets.items():
    cpu_info = PPP_CPU.get_part(value)

    with open("cpu.json", "a+") as outfile:
        json.dump(cpu_info, outfile)
