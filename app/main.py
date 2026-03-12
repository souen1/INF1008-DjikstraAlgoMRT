from data.mrt_graph import graph
from algorithms.dijkstra import dijkstra

def main():

    print("=== MRT Shortest Path Finder ===")

    print("\nAvailable Stations:")
    for station in sorted(graph.keys()):
        print("-", station)

    start = input("\nEnter start station: ")
    end = input("Enter destination station: ")

    if start not in graph or end not in graph:
        print("\nInvalid station name.")
        return

    distance, path = dijkstra(graph, start, end)

    if path:
        print("\nShortest Route:")
        print(" -> ".join(path))
        print(f"Total Distance: {distance}")
    else:
        print("No route found")

if __name__ == "__main__":
    main()