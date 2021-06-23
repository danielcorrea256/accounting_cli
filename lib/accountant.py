import uuid
from datetime import datetime, timedelta
from . import data_tools

HEADERS = ["uid", "date", "code", "detail", "debit", "credit", "balance"]


def register(values):
    """
    param: values [] array of info
    values should be well-ordered
    the i value of values[] should be pair to the headers
    """
    data = data_tools.get_data()
    new_record = {}

    # BECAUSE VALUES IS WELL-ORDERED
    # CREATES AN ENTRY IN THE DICT AND PUT THE i VALUE OF THE ARRAY 
    for i, header in enumerate(HEADERS):
        new_record[header] = values[i]
    
    data.append(new_record)
    data_tools.write_data(data, HEADERS)




def resume(start_date, final_date, filter_code=""):
    """
    params: start_date, final_date both are datetime values
    print data of incomes and expenses
    """
    data = data_tools.get_data()

    # FILTER ALL THE DATA RESPECT TO THE INTERVAL OF TIME
    resume_data = []
    if start_date and final_date:  
        for record in data:
            # GET THE DATE OF THE RECORD
            record_date = datetime.strptime(record["date"], "%d/%m/%Y")

            # PUT THE CODES TO EQUIAL LEN
            record_code = record["code"][:len(filter_code)]
            match_code = record_code == filter_code if filter_code else True

            # FILTER, IF THE RECORD MATCHES WITH THE SELECT PROPERTIES, APPEND TO resume data
            if start_date <= record_date <= final_date and match_code:
                resume_data.append(record)
    else:
        resume_data = data
    
    
    # RECOLECT DATA
    incomes = 0
    expenses = 0
    for record in resume_data:
        if record["code"][0] == "4":
            incomes += float(record["debit"])
        elif record["code"][0] == "5":
            expenses += float(record["credit"])

    # PRINT
    print("""
    ****************
    INCOMES: {}
    EXPENSES: {}
    ****************
    """.format(incomes, expenses))

    return resume_data




def monthly_resume(filter_code, delay=0):
    """
    do resume() getting the resume of current month
    first day of the current month as start date
    last day of the current month as final date
    """
    month = datetime.now().month - delay % 12
    year = datetime.now().year - delay // 12

    start_date = datetime(year, month, 1)
    final_date = datetime(year, month + 1, 1) - timedelta(1)

    return resume(start_date, final_date, filter_code)




def today_resume(n, filter_code = ""):
    return resume(datetime.now(), datetime.now(), filter_code)




def last_n_days_resume(n, filter_code = ""):
    start_date = datetime.now() - timedelta(n)
    final_date = datetime.now()

    return resume(start_date, final_date, filter_code)




def get_balance(code, debit=0, credit=0):
    """
    params: code str, debit float/int, credit float/int
    return: The credit - debit or viceversa, depending of the code
    of all the total records in the data
    """
    data = data_tools.get_data()    # GET DATA FROM "./register.csv"
    balance = 0     # INITIALIZE

    # 1 and 4 -> debit - credit
    # 2, 3 and 5 -> credit - debit
    if code[0] in ["2", "3", "5"]:
        balance = float(credit) - float(debit)
    else:
        balance = float(debit) - float(credit)

    for record in data:
        if code[0] in ["2", "3", "5"]:
            if record["code"] == code:
                balance += float(record["credit"])
                balance -= float(record["debit"])
        else:
            if record["code"] == code:
                balance += float(record["debit"])
                balance -= float(record["credit"])

    return balance




def balance_sheet():
    """
    Show the assets, liabilities and equity in all time
    """
    list_codes = data_tools.get_codes()
    
    assets = 0
    liabilities = 0

    for item in list_codes:
        code = item["code"]
        if code[0] == "1":
            assets += get_balance(code)
        elif code[0] == "2":
            liabilities += get_balance(code)
    
    equity = assets - liabilities

    print(assets)

    print("""
    *********************+
    ASSETS: {}
    LIABILITIES: {}
    EQUITY: {}
    """.format(assets, liabilities, equity))




def list_codes(filters = []):
    # GET THE LIST OF CODES
    codes = data_tools.get_codes()
    
    # PRINT HEADERS
    print("------- LIST OF CODES -------")
    try:
        headers = codes[0].keys()
    except IndexError:
        headers = ["code", "description"]
    
    text = " | "
    for header in headers:
        text += header + " | "
    print(text)

    # PRINT ROWS
    text = ""
    if len(filters) == 0:
        for item in codes:
            print(" | {} | {} | ".format(item["code"], item["description"]))
    else:
        for i in filters:
            for item in codes:
                if item["code"][0] == i:
                    print(" | {} | {} | ".format(item["code"], item["description"]))
    print()
        
    


def contra_entry(pre_code, debit, credit):
    """
    Params: precode str, debit str, credit str
    Each record has an contra entry
    A contra entry is a record related to another record
    the contra entry is based on the code of the previous record and debit/credit
    """
    # ******* GENERATE UID *******
    uid = uuid.uuid4()
    # ******** GENERATE TIME ********
    date = datetime.now().strftime("%d/%m/%Y")

    # ******** THE RELATED RECORD IS AN ACTIVE OF PASSIVE, THEN CONTRA ENTRY TO EQUITY **********
    if pre_code == "1" or pre_code == "2":
        balance = get_balance("3", debit, credit)
        register([uid, date, 3, "Contra entry", debit, credit, balance])
    # ********** THE RELATED RECORD IS AN INCOME, THEN CONTRA ENTRY ON ASSETS *****
    elif pre_code == "4":
        print("Where did the money go?")
        list_codes(["1"])   # SHOW THE ASSETS IN ORDER TO SELECT LATER
        code_ce = input("Select an asset[code]: ")
        data_tools.is_new_code(code_ce)
        balance = get_balance(code_ce, debit, credit)    # GET THE BALANCE OF code_ce
        register([uid, date, code_ce, "Contra entry of income", debit, credit, balance])
    # ************ THE RELATED RECORD IS AN EXPENSE, THEN CONTRA ENTRY ON ASSETS OR LIABILITIES
    elif pre_code == "5":
        print("From where did you get the money?")
        list_codes(["1", "2"])
        code_ce = input("[code]: ")
        data_tools.is_new_code(code_ce)
        balance = get_balance(code_ce, debit, credit)    # GET THE BALANCE OF code_ce
        if code_ce[0] == "1":
            register([uid, date, code_ce, "Contra entry", debit, credit, balance])
        elif code_ce[0] == "2":
            register([uid, date, code_ce, "Contra entry", debit, credit, balance])
