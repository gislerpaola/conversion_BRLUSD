#Calculating conversion

def conversion():
    while True:
        print("What is the amount? (Enter a non-positive value to exit)")
        try:
            amount = float(input().strip())
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if amount <= 0:
            break  # Exit the loop if the amount is 0 or negative

        # Ensure valid currency input
        while True:
            print("What is the currency? (Enter 'd' for dollar, 'r' for real)")
            currency = input().strip().lower()
            if currency in ["d", "r"]:
                break
            print("Invalid currency input. Please enter 'd' for dollars or 'r' for reals.")

        print("What's the dollar/real rate?")
        try:
            rate = float(input().strip())
            if rate <= 0:
                print("Rate must be a positive number.")
                continue
        except ValueError:
            print("Invalid rate. Please enter a valid number.")
            continue

        if currency == "d":
            converted = amount * rate  # First, convert the amount
            result = converted * 0.988  # Then apply the 1.2% fee
            print(f"Final amount received in reals: {result}")

        elif currency == "r":
            converted = amount / rate  # First, convert the amount
            result = converted * 0.988  # Then apply the 1.2% fee
            print(f"Final amount received in dollars: {result}")

conversion()
print("Pleasure doing business with you!")



