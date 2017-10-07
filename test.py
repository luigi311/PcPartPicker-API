from PcPartPicker import PPP_API

print("Total CPU pages:", PPP_API.get_total_pages("cpu"))

# Gets info on page 2
cpu_info = PPP_API.get_part("cpu", 2)

# Print the names of all the CPUs on page 2
for cpu in cpu_info:
    print(cpu["name"], ":", cpu["price"])
