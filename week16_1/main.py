import re

# Format the output
def format_sales(sales_data):
    lines = []
    for name, items in sales_data.items():
        item_str = ', '.join([f"{item}: {price}" for item, price in items.items()])
        lines.append(f"{name} buys {item_str}")
    return lines

def main():
    data = open('log.txt')

    # Dictionaries to store sales data
    vip_sales = {}
    member_sales = {}

    # Total sales counters
    total_sales = {}

    for line in data:
        if re.search('^\[VIP\] ', line) :
            # [VIP] Peter buys Notebook for $539
            name = re.findall("^\[VIP\] (\S\S+)", line)[0]
            item = re.findall(".+buys (\S\S+)", line)[0]
            price = re.findall("[0-9]+", line)[0]
            if name not in vip_sales.keys():
                vip_sales[name] = {}
            if item not in vip_sales[name]:
                vip_sales[name][item] = 0
            vip_sales[name][item] += int(price)
        else:
            name = re.findall("(\S\S+)", line)[0]
            item = re.findall(".+buys (\S\S+)", line)[0]
            price = re.findall("[0-9]+", line)[0]
            if name not in member_sales:
                member_sales[name] = {}
            if item not in member_sales[name]:
                member_sales[name][item] = 0
            member_sales[name][item] += int(price)
        
        if len(item) + len(price) > 0:
            if item not in total_sales.keys():
                total_sales[item] = 0
            total_sales[item] += int(price)

    output_lines = []
    output_lines.append("[VIP]")
    output_lines.extend(format_sales(vip_sales))

    output_lines.append("\n[Member]")
    output_lines.extend(format_sales(member_sales))

    output_lines.append(f"\nTotal Computer sales: {total_sales['Computer']}")
    output_lines.append(f"Total Notebook sales: {total_sales['Notebook']}")
    output_lines.append(f"Total Paper sales: {total_sales['Paper']}")
    output_lines.append(f"Total Book sales: {total_sales['Book']}")

    # Join output lines into final result string
    result = "\n".join(output_lines)

    # Print result
    print(result)

    # Write to file
    with open("Analysis_result.txt", "w") as f:
        f.write(result)

main()