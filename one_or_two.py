def one_or_two():
    print("Please specify if you are required data on Primary or Secondary schools")
    inp = input("Choose 1 for Primary or 2 for Secondary")
    if inp == "1":
        return "Primary"
        # whatevercodeyouwant_1()
    elif inp == "2":
        return "Secondary"
        # whatevercodeyouwant_2()
    else:
        print("You must choose between 1 or 2")
        return one_or_two()
