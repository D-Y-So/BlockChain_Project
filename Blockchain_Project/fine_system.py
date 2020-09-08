# Submitted by: Daria Yampolsky-Sokolov

import sys
import os
from web3 import Web3
import json

# variable declarations:
# --------------------------------------------------------------------

# address where the contract was deployed
contract_address = "0xfffeff360ce77502cf34ce9124566ae7230edcae"

# contract abi- Application Binary Interface, how you call functions in a contract and get data back
contract_abi = json.loads('[{"constant":true,"inputs":[{"name":"_fineId","type":"uint256"}],"name":"getFine","outputs":[{"name":"","type":"uint256"},{"name":"","type":"uint256"},{"name":"","type":"uint256"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"uint256"},{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"transferBalance","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getContractBalance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_fineId","type":"uint256"}],"name":"payFine","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getFineCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_ofId","type":"uint256"},{"name":"_license","type":"uint256"},{"name":"_plateNum","type":"uint256"},{"name":"_date","type":"string"},{"name":"_fineType","type":"string"},{"name":"_payAmount","type":"uint256"}],"name":"addFine","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_fineId","type":"uint256"},{"name":"_ofId","type":"uint256"},{"name":"_license","type":"uint256"},{"name":"_plateNum","type":"uint256"},{"name":"_date","type":"string"},{"name":"_fineType","type":"string"},{"name":"_payAmount","type":"uint256"},{"name":"_paid","type":"bool"}],"name":"editFine","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
# link to node connected to the ethereum ropsten network
infura_url = "https://ropsten.infura.io/v3/4908e696ba484070b0865832798d1e27"

account_1 = list()
key_1 = list()


# functions :
# ---------------------------------------------------------------

def func_login():
    flag = True
    while (flag == True):
        print("*******Welcome to Fine Management and Payment System*******\n")
        str_usr = input("Please enter username: ")
        str_pass = input("Please enter password: ")
        fp = open('users.txt', 'r')
        str_ln = fp.readline()
        lst = []
        chk = False
        while (str_ln and chk == False):
            lst = str_ln.split()
            if (lst[0] == str_usr and lst[1] == str_pass):
                chk = True
            str_ln = fp.readline()
        fp.close()

        if not chk:
            print("Wrong username or password!")
            choice = input("Press q to exit.\n Press any other key to try again: ")
            print('\n' * 80)
            os.system('cls')
            if (choice == "q"):
                flag == False
                func_exit()
        else:
            print('\n' * 80)
            os.system('cls')
            print("Authentication Complete.")
            account_1.append(lst[3])
            key_1.append(lst[4])
            if (lst[2] == "1"):
                func_issuer()
            elif (lst[2] == "2"):
                func_payer()
            else:
                print("No such user! Exiting System.")
                func_exit()


def func_issuer():
    end = False
    while (end is False):
        print('\n' * 80)
        os.system('cls')
        print("************MAIN MENU**************\n")

        choice = input("1: Add New Fine\n2: Edit Existing Fine\n3: View Fine\nQ: Quit\n\n   Please enter your choice: "
                       "")
        if choice == '1':
            add_fine()
        elif choice == '2':
            edit_fine()
        elif choice == '3':
            show_fine()
        elif choice == "Q" or choice == "q":
            end = True
            func_exit()
        else:
            print('\n' * 80)
            os.system('cls')
            print("You must only select 1,2,3 or Q.")
            print("Please try again")
            input("Press any key to continue...")


def func_payer():
    end = False
    while (end is False):
        print('\n' * 80)
        os.system('cls')
        print("************MAIN MENU**************\n")
        choice = input("1: Pay for Fine\n2: View Fine\nQ: Quit\n\n      Please enter your choice: ")

        if choice == '1':
            pay_fine()
        if choice == '2':
            show_fine()
        elif choice == "Q" or choice == "q":
            end = True
            func_exit()
        else:
            print('\n' * 80)
            os.system('cls')
            print("You must only select 1,2 or Q.")
            print("Please try again")
            input("Press any key to continue...")


def add_fine():
    end = False
    while (end == False):
        print('\n' * 80)
        os.system('cls')
        print("*******Add New Fine*******\n")
        lst_fine = list()

        # getting fine details from user:
        lst_fine.append(int(input("Enter offender's ID (9 digits only): ")))
        lst_fine.append(int(input("Enter offender's driving license (digits only): ")))
        lst_fine.append(int(input("Enter vehicle plate number (digits only): ")))
        lst_fine.append(str(input("Enter offense date in format DD/MM/YYYY: ")))
        lst_fine.append(str(input("Enter Fine Type: ")))
        lst_fine.append(float(input("Enter Payment Amount in Ether (positive decimal): ")))
        lst_fine.append(False)

        # convert ether to wei before sending transaction:
        pay_amount = web3.toWei(lst_fine[5], 'ether')

        # transaction details:
        nonce = web3.eth.getTransactionCount(account_1[0])
        tx = {
            'nonce': nonce,     # to prevent reusing transaction
            'gas': 2000000,     # gas limit
            'gasPrice': web3.eth.gasPrice  # gas price
        }

        # create transaction- activate contract function addFine with fine details given by user:
        txn = contract.functions.addFine(lst_fine[0], lst_fine[1], lst_fine[2], lst_fine[3], lst_fine[4], pay_amount).buildTransaction(tx)
        # sign transaction with private key:
        signed = web3.eth.account.signTransaction(txn, key_1[0])
        # get transaction hash:
        txn_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
        print("\ntransaction hash is: " + web3.toHex(txn_hash))

        # get transaction receipt:
        print("\nWaiting for the transaction receipt...")
        web3.eth.waitForTransactionReceipt(txn_hash)
        dict1 = web3.eth.getTransactionReceipt(txn_hash)
        print("\n****Transaction Receipt****")
        for x in dict1:
            print(x, ':', dict1[x])

        print("\nNew fine added successfully\n")

        # ask user if he wants to add another fine:
        choice = input("Add another fine? (y/n): ")
        if choice == 'y':
            print()
        elif choice == 'n':
            input("\nPress any key to return to Main Menu...")
            end = True
        else:
            print('\n' * 80)
            os.system('cls')
            print("You must only select 'n' or 'y'.")
            print("Please try again")
            input("Press any key to continue...")


# function for finding a fine that was added to the contract, using fine number given by user
def find_fine():
    fine_num = int(input("Enter fine number (digits only): "))

    # get latest fine number from the contract:
    fine_count = contract.functions.getFineCount().call()

    # check if user giver fine number exists:
    found = 0 < fine_num <= fine_count
    if (found == False):
        print("No fine with such number")
        return [-1, -1, True]
    else:
        print("Fine Found:\n")

        # get fine details from contract with given fine number
        fine_lst = contract.functions.getFine(fine_num).call()

        # show fine details:
        print("Fine Number: " + str(fine_num) + "\n")
        print("Offender ID: " + str(fine_lst[0]) + "\n")
        print("Driving License: " + str(fine_lst[1]) + "\n")
        print("Vehicle plate number: " + str(fine_lst[2]) + "\n")
        print("Offense Date: " + str(fine_lst[3]) + "\n")
        print("Fine Type: " + str(fine_lst[4]) + "\n")
        print(
            "Payment Amount: " + str(web3.fromWei(fine_lst[5], 'ether')) + " ETH (" + str(fine_lst[5]) + " wei)" + "\n")
        if (fine_lst[6] == False):
            print("Paid: No\n")
        else:
            print("Paid: Yes\n")

        return [fine_num, fine_lst[5], fine_lst[6]]

def show_fine():
    end = False
    while (end == False):
        print('\n' * 80)
        os.system('cls')
        print("*******View Fines*******\n")

        # find the required fine using fine number:
        find_fine()

        # ask user if he wants to view another fine:
        choice = input("Find another fine? (y/n): ")
        if str(choice) == 'y':
            print()
        elif str(choice) == 'n':
            input("Press any key to return to Main Menu...")
            end = True
        else:
            print('\n' * 80)
            os.system('cls')
            print("You must only select 'n' or 'y'.")
            print("Please try again")
            input("Press any key to continue...")


def edit_fine():
    end = False
    while (end == False):
        print('\n' * 80)
        os.system('cls')
        print("*******Edit Fine*******\n")

        # find fine
        fine = find_fine()

        # check if fine exists:
        if (fine[0] > 0):
            # check if fine was paid:
            if (fine[2] == True):
                print("\nCan't edit paid fine! Returning to Main Menu.")
                input("Press anu key to continue...")
                end = True
            else:
                print("\nYou can now edit the fine:\n")
                lst_fine = list()
                # getting new details from user:
                lst_fine.append(int(input("Enter offender's ID (9 digits only): ")))
                lst_fine.append(int(input("Enter offender's driving license (digits only): ")))
                lst_fine.append(int(input("Enter vehicle plate number (digits only): ")))
                lst_fine.append(str(input("Enter offense date in format DD/MM/YYYY: ")))
                lst_fine.append(str(input("Enter Fine Type: ")))
                lst_fine.append(float(input("Enter Payment Amount in Ether (positive decimal): ")))
                lst_fine.append(False)

                # convert ether to wei before sending transaction:
                pay_amount = web3.toWei(lst_fine[5], 'ether')

                # transaction details:
                nonce = web3.eth.getTransactionCount(account_1[0])
                tx = {
                    'nonce': nonce,  # to prevent reusing transaction
                    'gas': 2000000,  # gas limit
                    'gasPrice': web3.eth.gasPrice  # gas price
                }

                # create transaction- activate contract function addFine with fine details given by user:
                txn = contract.functions.editFine(fine[0], lst_fine[0], lst_fine[1], lst_fine[2], lst_fine[3], lst_fine[4],pay_amount,lst_fine[6]).buildTransaction(tx)
                # sign transaction with private key:
                signed = web3.eth.account.signTransaction(txn, key_1[0])
                # get transaction hash:
                txn_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
                print("\ntransaction hash is: " + web3.toHex(txn_hash))

                # get transaction receipt:
                print("\nWaiting for the transaction receipt...")
                web3.eth.waitForTransactionReceipt(txn_hash)
                dict1 = web3.eth.getTransactionReceipt(txn_hash)
                print("\n****Transaction Receipt****")
                for x in dict1:
                    print(x, ':', dict1[x])

                print("\nFine was edited successfully\n")

                # ask user if he wants to add another fine:
                choice = input("Edit another fine? (y/n): ")
                if choice == 'y':
                    print()
                elif choice == 'n':
                    input("\nPress any key to return to Main Menu...")
                    end = True
                else:
                    print('\n' * 80)
                    os.system('cls')
                    print("You must only select 'n' or 'y'.")
                    print("Please try again")
                    input("Press any key to continue...")
        else:
            print("No fine with given Number! Returning to Main Menu")
            input("Press any key to continue...")
            end = True


def pay_fine():
    print('\n' * 80)
    os.system('cls')
    print("*******Pay for Fines*******\n")
    fine = find_fine()

    balance = web3.eth.getBalance(account_1[0])
    print("Your account balance: " + str(web3.fromWei(balance, 'ether')) + " ETH (" + str(balance) + " wei)" + "\n")

    # check if fine was found:
    if (fine[0] > 0):
        # check if fine was paid:
        if (fine[2] == True):
            print("Fine was already paid!\nReturning to Main Menu.\n")
        # check if paying account has enough ether:
        elif (balance <= fine[1]):
            print("Not enough Ether for fine payment and transaction fee!\nReturning to Main Menu.\n")
        # if fine was found, fine not paid and enough ether in account, you can pay the fine:
        else:
            print("Fine pay amount: " + str(web3.fromWei(fine[1], 'ether')) + " ETH (" + str(fine[1]) + " wei)")
            choice = input("Do you wish to pay the fine? (y/n): ")
            if str(choice) == 'y':
                print("\npaying for fine number " + str(fine[0]) + " ...")

                # preparing transaction:
                nonce = web3.eth.getTransactionCount(account_1[0])  # prevent double spend problem
                tx = {
                    'nonce': nonce,
                    'value': fine[1],               #amount of ether transferred to the account (in wei)
                    'gas': 2000000,                 #gas limit
                    'gasPrice': web3.eth.gasPrice,  #gas price
                }  # transaction

                # create transaction- activate contract function addFine with fine details given by user:
                txn = contract.functions.payFine(int(fine[0])).buildTransaction(tx)
                # sign transaction with private key:
                signed = web3.eth.account.signTransaction(txn, key_1[0])
                # get transaction hash:
                txn_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
                print("\ntransaction hash is: " + web3.toHex(txn_hash))

                # get transaction receipt:
                print("\nWaiting for the transaction receipt...")
                web3.eth.waitForTransactionReceipt(txn_hash)
                dict1 = web3.eth.getTransactionReceipt(txn_hash)
                print("\n****Transaction Receipt****")
                for x in dict1:
                    print(x, ':', dict1[x])

                print("\nPayment for fine number " + str(fine[0]) + " was successful!")
                print("You can see that the fine was paid in the 'Show Fine' section in the Main Menu.\n")
            elif str(choice) == 'n':
                print("No payment was executed!")
            else:
                print('\n' * 80)
                os.system('cls')
                print("You must only select 'n' or 'y'.")
                print("No payment was executed!")
    input("Press any key to return to Main Menu...")

def func_exit():
    print('\n' * 80)
    os.system('cls')
    input("Exited System.\nPress any key to continue... ")
    sys.exit()


# running the program:
# ---------------------------------------------------------------------

web3 = Web3(Web3.HTTPProvider(infura_url))
if (web3.isConnected()):
    print("Connected to Ropsten Blockchain Network!")
else:
    print("Error connecting to Ropsten Blockchain Network! Restart program.")
    func_exit()

# address where the contract was deployed
contract_address = web3.toChecksumAddress(contract_address)

# instantiate contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

#print(contract.functions.getContractBalance().call())

func_login()