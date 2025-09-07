# Python assignment

Welcome to this home assignment!

This exercise have several goals:
- Ensure that you can produce some quality code
- Serve as a base for an open-discussion for our next interview about your choices
 
## Guidelines

-  We don't want you to spend 10 hours on it, two hours at max should be enough (any tool/AI is allowed). If there are enhancements that you want to add but it takes too much time, you can list them in a README file (be as specific as possible). A specific TODO point is better than a bad piece of code.
-  The specifications are voluntarily open (e.g. for naming, parameters), so you can do whatever seems a good idea to you. Feel free to adapt/enhance/ensure consistency.
- Adding tests is good.
- Send back the result in the format/method of your choice.

## Exercise

The exercise is to build a backend serving a REST API in Python. You can choose whatever stack you want (but it has to be in Python). 

- The underlying app have a database (stick to a local db in sqlite), with a single model whose columns are:
	- column_1, column_2, ... (it's up to you to decide how many columns you create)
	- each column's type is integer 
- At startup, the app must create the table and add some rows with random values.

### Endpoint 1

We want a first endpoint that should 
- allow the client to add two columns (row by row), with the possibility to specify these columns
	- Example: to add column_1 and column_5, the payload could look like {"the_first_col_name":"column_1", "my_second_colname": "column_5"}).
- provide the output as a list of values (i.e. the resulting column)
	- example: if column_1 is [1,2,3] and column_5 is [4,5,6], the result would be [5,7,9]

### Endpoint 2

The second endpoint is an enhanced version of the first endpoint. It should allow the client to pass a formula as a string. For example, the client should be able to call the endpoint with the payload {"myFormula": "column_1 + column_2 * column_3"}
- the output is also a list of values (i.e. the resulting column)
