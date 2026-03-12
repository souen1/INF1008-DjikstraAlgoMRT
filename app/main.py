from data.mrt_graph import graph
from algorothms.djikstra import dijkstra

def main():

    print("=== MRT Shortest Path Finder ===")

    print("\nAvailable Stations:")
    for station in graph.keys():
        print("-", station)

    start = input("\nEnter start station: ")
    end = input("Enter destination station: ")

    distance, path = dijkstra(graph, start, end)

    if path:
        print("\nShortest Route:")
        print(" -> ".join(path))
        print(f"Total Distance: {distance}")
    else:
        print("No route found")

if __name__ == "__main__":
    main()