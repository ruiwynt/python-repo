import sys
from pprint import PrettyPrinter

from flow_digraph import FlowDigraph

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("pass path to graph file as argument")
        sys.exit(1)

    G = FlowDigraph()
    G.read_flow_digraph(sys.argv[1])
    G.max_flow()
    print(G.get_flow())
    PrettyPrinter(indent=2, width=1).pprint(G.flows)
