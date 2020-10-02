import random
import sqlite3

acc_num = 0
acc_pin = 0

conn = sqlite3.connect('card.s3db')
c = conn.cursor()


def create_table():
    c.execute("DROP TABLE card")
    c.execute('''CREATE TABLE "card" (
                    "id" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
                    "number" TEXT, 
                    "pin" TEXT, 
                    "balance" INTEGER DEFAULT 0);''')
    conn.commit()


def read_card(num_in, pin_in):
    if type(pin_in) == str:
        c.execute("SELECT card.number, card.pin, balance "
                  "FROM card "
                  "WHERE card.number =? AND card.pin =?",
                  (num_in, pin_in))
    elif pin_in == 0:
        c.execute("SELECT card.number, balance "
                  "FROM card "
                  "WHERE card.number =? AND balance >= ?",
                  (num_in, 0))
    ls = c.fetchone()
    return ls


def gen_acc():
    global acc_num, acc_pin
    acc_id = str(random.randint(1000000000, 2000000000))    # Can have separate function called generate_acc_id
    acc_id = '0' + acc_id[1:]
    acc_num = "40000" + acc_id
    acc_num = check_luhn(acc_num, 0)
    acc_pin = str(random.randint(10000, 20000))     # Can have separate function called generate_acc_pin
    acc_pin = '' + acc_pin[1:]
    c.execute("INSERT INTO card (number, pin) VALUES (?, ?)", (acc_num, acc_pin))
    conn.commit()
    return acc_num, acc_pin


def check_luhn(num, com):
    global acc_num
    count = 0
    sum = 0
    for x in num:
        if count % 2 == 0:
            x = int(x) * 2
            if x > 9:
                x -= 9
        sum += int(x)
        count += 1
    if com == 0:
        return acc_num + str(10 - (sum % 10)) if sum % 10 > 0 else '0'
    elif com == 1:
        if sum % 10 != 0:
            return True
        else:
            return False


def update_bal(amount, num, com):
    change = (amount, num)
    if com == 0:
        query = "UPDATE card SET balance = balance + ? WHERE number = ?"
    elif com == 1:
        query = "UPDATE card SET balance = balance - ? WHERE number = ?"
    c.execute(query, change)
    conn.commit()
    return c.fetchone

create_table()

while True:
    choice = input("1. Create an account \n2. Log into account \n0. Exit \n")
    if choice == '1':
        gen_acc()
        print("\nYour card has been created")
        print("Your card number:")
        print(acc_num)
        print("Your card pin:")
        print(acc_pin)
    elif choice == '2':
        t_num = input("Enter your card number:\n")
        t_pin = input("Enter you PIN:\n")
        data = read_card(t_num, t_pin)
        if data is not None:
            print("You have successfully logged in!")
            while True:
                choice = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
                if choice == '1':
                    data = read_card(t_num, t_pin)
                    print(data[2])
                elif choice == '2':
                    update_bal(input("Enter income:\n"), t_num, 0)
                    print("Income was added!")
                elif choice == '3':
                    trans_num = input("Transfer\nEnter card number:\n")
                    ls = read_card(trans_num, 0)
                    if check_luhn(trans_num, 1):
                        print("Probably you made mistake in the card number. Please try again!")
                        continue
                    elif ls is None:
                        print("Such a card does not exist.")
                        continue
                    elif len(ls[0]) != 16:
                        print("Probably you made mistake in the card number. Please try again!")
                        continue
                    elif trans_num == t_num:
                        print("You can't transfer money to the same account!")
                        continue
                    else:
                        ls = read_card(t_num, 0)
                        amount = int(input("Enter how much money you want to transfer:\n"))
                        if ls[1] < amount:
                            print("Not enough money!")
                            print(ls[1])
                            continue
                        else:
                            update_bal(amount, t_num, 1)
                            update_bal(amount, trans_num, 0)
                            print("Success!")
                elif choice == '4':
                    c.execute("DELETE FROM card WHERE number = ? AND pin = ?;", (t_num, t_pin))
                    conn.commit()
                    break
                elif choice == '5':
                    print("You have successfully logged out!")
                    break
                elif choice == '0':
                    print("Bye!")
                    exit()
        else:
            print("Wrong card number or PIN!")
    elif choice == '0':
        print("Bye!")
        exit()
