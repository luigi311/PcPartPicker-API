from PcPartPicker import PPP_API

cpu_info = PPP_API.get_item("cpu")

for cpu in cpu_info:
    print(cpu)
