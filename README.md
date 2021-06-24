# accounting_cli

`accounting_cli` is a command line interface application used to personal finances, this involves some accounting ideas

# Use

`accounting_cli` has a interface when you execute the python file `python accounting_cli.py`

The interface guides you

## Gifs

![gif](/gifs/create.gif)
![gif](/gifs/create2.gif)
![gif](/gifs/resume.gif)

## Accounting ideas 

`accounting_cli` use terms as debit, credit, balance, contra_entry
For example: If you register an asset, the value is recorded in the debit and then a record in the equity is made(btw, don't register equity by yourself)

### Codes

Codes are the way of clasify an activity of the personal finances, if it is a income, a expense, etc
Codes can be more complex, but, the first digits of the code tells us about its meaning

The first digit of the code has information about the code itself

Code | Meaning
---  | ---
1    | Asset
2    | Liability
3    | Equity
4    | Incomes
5    | Expenses

There are some codes by default

Code | Meaning
---  | ---
11   | bank account
12   | cash
13   | receivable
21   | Loan
22   | Credit
41   | Gift
51   | Buy food
52   | Uber
53   | Bus
