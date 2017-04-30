# AMI-Assignmant
**2017 Artificial Machine Intelligence Assignment. Curtin University**

*This assignment was to implement an informed beam search, and simplified memory limited A \* search.*

## Beam Search
The search can be run using the script named `beam-search`. This was as oer the assignment specification.
The script specifies the adjacency list and heuristic files, the source and destination nodes, the $k$ value, continued search and print verbose options.

## SMA* Search
The search can be run using the script named `alim-search`. This was as oer the assignment specification.
The script specifies the adjacency list and heuristic files, the source and destination nodes and print verbose options. The memory limitation in nodes, is stored as a constant in the python code.

## Testing
The saerches were tested well. Both will return correct solutions, with the SMA* returning all optimal solutions. The code was also tested on hundreds of randomly generated graphs. They were generated using [this tool.](https://github.com/LukeHealy/graph-gen)
Check out the report for known issues etc.

## Are the implementations correct?
I think so... There aren't many people who have the faintest clue as to how SMA* actually works, or how to go about implementing it. Most pseudo code on the subject is icomplete or incorrect.

The beam search is correct, it is quite simple.