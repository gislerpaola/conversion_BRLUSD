# Currency Conversion Program

This program allows users to convert an amount between USD (dollars) and BRL (reais), applying a 1.2% fee on the final result. The user inputs the amount, the currency (USD or BRL), and the exchange rate, and the program returns the converted amount after the fee is applied.

## Requirements

Python 3.6 or higher

## How to Use

Run the script: Execute the program in your terminal or command line.
Input Amount: Enter the amount you'd like to convert. To exit the program, enter a non-positive value.
Choose Currency: Choose between 'd' for dollars or 'r' for reais.
Enter Exchange Rate: Input the exchange rate for the selected currency. The program will automatically calculate the conversion and apply a 1.2% fee to the result.

## Features

Currency Conversion: Convert between USD and BRL.
Fee Calculation: The program applies a 1.2% fee to the conversion amount.
Input Validation: The program checks for valid numeric inputs and ensures the currency and rate are correctly entered.

## Code Overview

conversion() Function

The function uses a while loop to repeatedly ask for inputs until a non-positive value is entered for the amount.
It handles invalid inputs gracefully, prompting the user to enter correct data if necessary.
It performs the conversion based on the currency and applies the 1.2% fee before displaying the result.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
