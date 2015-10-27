Solution for the graph problem.
=====================
Written and tested with python 3.5. 
How to run test
---------------------
Use `$ python3.5 setup.py tests` to run the tests.
Example of input csv file
---------------------

```
A,B,5
B,C,4
C,D,8
D,C,8
D,E,6
A,D,5
C,E,2
E,B,3
A,E,7
```


Usage
---------------------
The packages goes with command line utility (with alias `graph`) witch has following commands:

####**distance** 
arguments: 
 
- `positional argument` - path to CSV file with graph 
- `-r/--route` - vertices separated by comma
 
example of usage:

- `$ graph distance ./input.csv --route A,E,B,C` - prints the distance of the route A­E­B­C­D
- `$ graph distance ./input.csv -r A,C` - prints the distance of the route A­D

####**shortest-path** 
- `positional argument` - path to CSV file with graph 
- `-s/--start` - start vertex
- `-e/--end` - end vertex

example of usage:
 
- `$ graph shortest-path ./input.csv --start A --end B` - prints the shortest path from A to B
- `$ graph shortest-path ./input.csv -s E -e A` - prints the shortest path from E to A
  
 If there is no such path - prints inf (Infinity)
   
####**paths-by-stops** 
Returns number of trips between two vertices with a maximum (less or equal, depends on operator) of N stops.

- `positional argument` - path to CSV file with graph 
- `-s/--start` - start vertex
- `-e/--end` - end vertex
- `-o/--operator` - operator for filtering results. Possible choices are: '<', '<=', '=='
- `-v/--value` - max number of stops

example of usage:
 
- `$ graph paths-by-stops ./input.csv --start C --end C --operator '<=' --value 3` - prints number 
of different routes starting at C and ending at C with a *maximum* of 3 stops
- `$ graph paths-by-stops ./input.csv -s E -e B -o '<' -v 4` - prints number 
of different routes starting at E and ending at B *with less than* 4 stops 
- `$ graph paths-by-stops ./input.csv --start A --end E --operator '==' --value 3` - prints number 
of different routes starting at A and ending at E *with exactly* 3 stops 
   
####**paths-by-distance** 
Returns number of trips between two vertices with a maximum (less or equal, depends on operator) distance of N.

- `positional argument` - path to CSV file with graph 
- `-s/--start` - start vertex
- `-e/--end` - end vertex
- `-o/--operator` - operator for filtering results. Possible choices are: '<', '<=', '=='
- `-v/--value` - max distance

example of usage:
 
- `$ graph paths-by-distance ./input.csv --start C --end C --operator '<' --value 30` - prints number 
of different routes starting at C and ending at C with a length *less than* 30
- `$ graph paths-by-distance ./input.csv -s E -e B -o '<=' -v 17` - prints number 
of different routes starting at E and ending at B with a *maximum* length of 17
- `$ graph paths-by-distance ./input.csv --start A --end E --operator '==' --value 7` - prints number 
of different routes starting at A and ending at E with a length *equal to* 7

