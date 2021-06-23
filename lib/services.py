import uuid
from datetime import datetime
from . import accountant
from . import data_tools

HEADERS = ["uid", "date", "code", "detail", "debit", "credit", "balance"]


def create_record():
    print("""
    **************************
        CREATING NEW RECORD...
    
    **************************
    """)
    # ***** UID *********
    uid = uuid.uuid4()
    # ****** DATE **********
    print("")
    date = input("Record's date [dd/mm/yyyy] Today as default: ")
    date = date if date else datetime.now().strftime("%d/%m/%Y")

    # ********** CODE **********
    print("Clasify this record with a code, or create a new code")
    accountant.list_codes()
    code = input("Code: ")
    data_tools.is_new_code(code)

    # ********** DETAIL ************
    print("")
    detail = input("Any detail that you want to add: ")

    # ********* DEBIT AND CREDIT *********
    money = input("How much money register?: ")
    debit = money if code[0] in ["1", "4"] else "0"
    credit = money if code[0] in ["2", "5"] else "0"

    # *********** BALANCE **************
    balance = accountant.get_balance(code, debit, credit)
    # ******** CONTRA ENTRY ***********
    accountant.contra_entry(code[0], credit, debit)

    # REGISTER
    accountant.register([uid, date, code, detail, debit, credit, balance])
    print()
    print("Record registered Sucesfull")
    print("*" * 30)



def create_resume():
    """
    Display an resume of the records
    """
    # ******** SELECT A FILTER FOR THE RECORD'S DATE ********
    print("""
    Select a filter of time
    [Enter] All time
    [M] Monthly resume
    [T] Today resume
    [n] Last n Days resume
    [I] An especific interval of time
    """)
    option = input("Option: ")

    # ********** SELECT A FILTER FOR THE RECORD'S CODE *********
    print("""
    ************************************
    Filter by code, enter to pass
    
    """)
    accountant.list_codes()
    filter_code = input("Enter to no filter or [code]: ")

    # ********* DEPENDING IN WHICH CASE, DISPLAY A RESUME
    if not option:
        resume = accountant.resume(None, None)
        show_resume(resume)
    elif option.upper() == "M":
        resume = accountant.monthly_resume(filter_code)
        show_resume(resume)     # show_resume(resume) prints resume in a good way
    elif option.upper() == "T":
        resume = accountant.today_resume(filter_code)
        show_resume(resume)
    elif option.upper() == "I":
        s_date_str = input("Select the start date of the interval [dd/mm/yyyy]: ")
        f_date_str = input("Select the final date of the interval [dd/mm/yyyy]: ")

        start_date = datetime.strptime(s_date_str, "%d/%m/%Y")
        final_date = datetime.strptime(f_date_str, "%d/%m/%Y")

        resume = accountant.resume(start_date, final_date, filter_code)
    # THE OPTION MAYBE IS AN INT n, TRY TO GET THE RESUME OF THE LAST n DAYS
    else:
        try:
            option = int(option)
            if option > 0:
                resume = accountant.last_n_days_resume(option, filter_code)
                show_resume(resume)
            else:
                raise ValueError("No valid interval")
        except ValueError:
            print("No valid option")
    
    


def show_resume(resume):
    print("""
    ****** RECORDS ******
    """)
    text = " | "

    try:
        for record in resume:
            record.pop("detail")
        for header in resume[0].keys():
            if header == "uid":
                spaces = 36 - len(header)
            else:
                spaces = 12 - len(header) if 12-len(header) > 0 else 0

            text += header + (" " * spaces)  + " | " 

    except IndexError:
        print("There is no data")
        return
    
    print(text)
    for record in resume:
        text = " | "
        for value in record.values():
            if len(value) < 12:
                spaces = 12 - len(value)
                text += value + (" " * spaces) + " | "
            else:
                text += value + " | "

        print(text)



def search_record():
    print("""
    ****** SEARCH A RECORD ********
    """)
    uid = input("Record's uid: ")

    data = data_tools.get_data()
    print("Looking for record ...")
    for record in data:
        if record["uid"] == uid:
            print("\nRECORD FOUND\n")
            for header, value in record.items():
                print("{}:{}".format(header, value))
            return
    print("\nRecord doesn't found\n")


def update_record():
    print("""
    ****** UPDATING A RECORD ********
    """)
    uid = input("Record's uid: ")

    data = data_tools.get_data()

    print("Looking for record ...")
    for record in data:
        if record["uid"] == uid:
            print("Record found, enter for keep value")
            for header, old_value in record.items():
                new_value = input("New {}: ".format(header)).strip()
                record[header] =  new_value if new_value else old_value
            data_tools.write_data(data, HEADERS)
            print("Record Updated")
            return
    print("Record doesn't found")




def delete_record():
    print("""
    ******** DELETING A RECORD ********
    """)
    uid = input("Record's uid: ")

    data = data_tools.get_data()

    print("Looking for record ... ")
    for record in data:
        
        if record["uid"] == uid:
            data.remove(record)
            data_tools.write_data(data, HEADERS)
            print("Record deleted")
            return
    print("Record doesn't found")




def create_balance_sheet():
    accountant.balance_sheet()
