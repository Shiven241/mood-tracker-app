secret_number=9
Guess_count=0
guess_limit = 3
while Guess_count< 3:
    guess= int(input( 'Guess: '))
    Guess_count += 1
    if guess == secret_number:
        print("You won!")
        break
    else:
        if Guess_count < guess_limit:
            print("Try again")
        else:
            print("You failed!")