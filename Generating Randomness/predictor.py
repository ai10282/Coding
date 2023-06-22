import random

min_num = 100
counter = 0
money = 1000
binary_string = ""
dict_triads = {"000": [0, 0], "001": [0, 0], "010": [0, 0], "011": [0, 0], "100": [0, 0], "101": [0, 0],
               "110": [0, 0], "111": [0, 0]}

print("Please provide AI some data to learn...")
while counter < min_num:
    print("The current data length is " + str(counter) + ", " + str(min_num - counter) + " symbols left")
    print("Print a random string containing 0 or 1:")
    print()
    random_string = input()
    for i in random_string:
        if i == "1" or i == "0":
            binary_string += i
    counter = len(binary_string)


print()
print('Final data string:')
print(binary_string)
print()
print("""You have $1000. Every time the system successfully predicts your next press, you lose $1. 
Otherwise, you earn $1. Print "enough" to leave the game. Let's go!""")
print()

for triads in dict_triads:
    i = 0
    while i < len(binary_string)-3:
        if binary_string[i] + binary_string[i+1] + binary_string[i+2] == triads:
            if binary_string[i+3] == "0":
                dict_triads[triads][0] += 1
            else:
                dict_triads[triads][1] += 1
        i += 1

while True:
    test_string = ""
    print("Print a random string containing 0 or 1:")
    print()
    input_string = input()
    if input_string == "enough":
        print("Game over!")
        break
    for i in input_string:
        if i == "1" or i == "0":
            test_string += i
    if len(test_string) < 4:
        print("some wrong input")
        print()
        test_string = ""
        continue

    prediction_string = ""
    j = 0
    while j < len(test_string) - 3:
        tri = test_string[j] + test_string[j+1] + test_string[j+2]
        for triads in dict_triads:
            if triads == tri:
                if dict_triads[triads][0] > dict_triads[triads][1]:
                    prediction_string += "0"
                elif dict_triads[triads][0] < dict_triads[triads][1]:
                    prediction_string += "1"
                else:
                    prediction_string += str(random.randint(0, 1))
        j += 1

    print("predictions:")
    print(prediction_string)
    print()

    test_string = test_string[3:]
    counter_test = 0
    k = 0
    while k < len(prediction_string):
        if test_string[k] == prediction_string[k]:
            counter_test += 1
        k += 1

    N = counter_test
    M = len(prediction_string)
    ACC = round((N/M) * 100.0, 2)
    print("Computer guessed " + str(N) + " out of " + str(M)
          + " symbols right (" + str(ACC) + " %)")
    money = money - N + (M - N)
    if money <= 0:
        print("Your balance is now $0")
        print("Game over!")
        break
    print("Your balance is now $" + str(money))

    for triads in dict_triads:
        i = 0
        while i < len(test_string) - 3:
            if test_string[i] + test_string[i + 1] + test_string[i + 2] == triads:
                if test_string[i + 3] == "0":
                    dict_triads[triads][0] += 1
                else:
                    dict_triads[triads][1] += 1
            i += 1
    print()
