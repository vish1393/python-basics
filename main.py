import random


def input_example():
    print("Welcome to the Band name generator")
    name = input("Name of the city you grew up?\n")
    print(name)
    pet = input("Name of Pet?\n")
    print(pet)
    print("Your Band name could be " + name + " " + pet)

def number_data_types_example():
    print("Welcome to the Tip calculator!")
    bill = float(input("What was the total Bill?\n"))
    print(bill)

    tip = int(input("How much tip would you like to give?\n 5, 10, 15, 20\n"))
    print(tip)

    split = int(input("How many people to split the bill\n"))
    print(split)

    total_bill = float(0)

    if int(tip) > 0:
        total_bill = bill + (bill * (tip / 100))

    per_person = round(total_bill / (split or 1), 2)

    print("Each person has to pay " + str(per_person))

def primitive_data_type_example():
    print(len("Hello"))
    print("Hello"[0])
    print("Hello"[-1])
    print(float("123.435")+int("34567565765765"))
    print(True)

def mathematical_data_types_example():
    print(123 + 456)
    print(3 * 2)
    print(5 - 2)
    print(5 / 3)
    print(5 // 3)
    print(2 ** 3)

    bmi = 84 / (1.655 ** 2)
    print(bmi)
    print(round(bmi))
    print(round(bmi, 2))
    print(type(bmi))

def number_operations():
    score = 0
    score += 1
    print(score)

    score = 4
    score -= 1
    print(score)

    score = 4
    score *= 2
    print(score)

    score = 4
    score /= 2
    print(score)

def if_else_example():
    print("Welcome to the Roller Coaster !!")
    height = int(input("Mention your height in cms ?"))

    if height >= 120:
        print("Get ready to ride !!")
        age = int(input("Mention your age in yrs ?"))
        ticket_price = 0

        if age <= 12:
            #print("Please pay 5$")
            ticket_price = 5
        elif age <= 18:
            #print("Please pay 7$")
            ticket_price = 7
        elif 45 <= age <= 55:
            ticket_price = 0
        else:
            #print("Please pay 12$")
            ticket_price = 12

        photo = (input("Do you need photo of the ride?"))

        if photo in ["y","yes"]:
            ticket_price += 3

        print(f"The total bill is: {ticket_price}")

    else:
        print("Sorry, you can't ride :(")

def do_while_example():
    num = 0
    while True:
        print(num)
        num += 1
        if num == 50:
            break

def gen_random_numbers():
    a = input("Head or Tail\n")
    ran = random.randint(0,1)
    if ran == 1:
        print("Its Tail")
    else:
        print("its Head")

def for_loop_example():
    numbs=[1,2,3,4,10]
    for x in numbs:
        print(x)


scores = [180, 29, 75, 89, 100, 250, 99, 150]

max_scores = 0
for sc in scores:
    if sc > max_scores:
        max_scores = sc
print(max_scores)

temp = 0
for i in range(1,101):
    temp = temp + i
print(temp)
