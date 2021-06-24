import csv 

DATA_FILE = "lib/register.csv"
CODES_FILE = "lib/codes.csv"


def get_data():
    """
    reads the data file and return the data as an array[]
    this array contains dicts, each dict is a record
    """
    try:
        with open(DATA_FILE, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data = []
            for row in csv_reader:
                data.append(row)
            return data

    # IF THE FILE IS NOT IN THE RIGHT PATH OR IS DELETED, RETURN {}
    except FileNotFoundError:
        return []   




def write_data(new_data, headers):
    """
    Modify the data file
    params: new_data is an array of dicts[{h1:v1, h2:v2, ...},{...},...]
    each dict is a record
    """
    with open(DATA_FILE, mode="w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = headers)
        writer.writeheader()
        for record in new_data:
            writer.writerow(record)




def is_new_code(code):
    """
    Verify if "code" is a valid code or if you want to create it
    """
    new_code = True
    codes = get_codes()
    for item in codes:
        if code == item["code"]:
            new_code = False
    if new_code:
        create = input("Do you want to create a new code?[y/n]: ")
        if create.upper() == "Y":
            description_code = input("Description of the new code: ")
            codes.append({"code": code, "description": description_code})
            write_codes(codes)
        else:
            raise ValueError("Invalid Code")




def sort_codes(data):
    """
    return: an array of dicts sorted by the attribute["code"]
    sorted alphabetically
    """
    is_sorted = False
    while not is_sorted:
        change = False
        for i in range(len(data) - 1):
            if data[i]["code"] > data[i + 1]["code"]:
                x = data[i]
                data[i] = data[i + 1]
                data[i + 1] = x
                change = True
        is_sorted = not change
    return data




def get_codes():
    """
    return: an array of dicts [{"code": xxx, "description": xxx}, ...]
    """
    try:
        with open(CODES_FILE, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            print("ok")
            data = []
            for row in csv_reader:
                data.append(row)
            return sort_codes(data)
    # IF THE FILE IS NOT IN THE RIGHT PATH OR IS DELETED, RETURN {}
    except FileNotFoundError:
        print("Codes doesn't founded")
        return []




def write_codes(new_codes):
    """
    Modify file ./codes.csv
    params: new_codes is an array of dicts [{"code": xxx, "description": xxx}, ...]
    """
    with open(CODES_FILE, mode="w") as csv_file:
        new_codes = sort_codes(new_codes)
        writer = csv.DictWriter(csv_file, fieldnames = ["code", "description"])
        writer.writeheader()
        for code in new_codes:
            writer.writerow(code)

