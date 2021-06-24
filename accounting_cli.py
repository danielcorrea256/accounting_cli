from lib import services

def main():
    print("""
    **************************************
    Hello, what do you want to do?
    [1] Record
    [2] See the resume

    [3] Search a record by uid
    [4] Update a record [Not recommended]
    [5] Delete a record [Not recommended]

    [6] Show balance sheet
    
    **************************************
    """)
    option = input("Option: ")

    if option == "1":
        services.create_record()
    elif option == "2":
        services.create_resume()
    elif option == "3":
        services.search_record()
    elif option == "4":
        services.update_record()
    elif option == "5":
        services.delete_record()
    elif option == "6":
        services.create_balance_sheet()

main()