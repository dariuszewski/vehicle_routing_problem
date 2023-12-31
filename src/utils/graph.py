# some graphs
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def generate_nx_graph(fleet):
    # Create a new graph
    plt.figure(figsize=(15, 8))
    G = nx.Graph()

    # Map for vehicle colors
    vehicle_colors = {}
    colors = ['blue', 'green', 'red', 'yellow', 'purple', 'orange', 'black']
    color_index = 0

    for vehicle in fleet:
        # Assign a color for each vehicle
        vehicle_color = colors[color_index % len(colors)]
        vehicle_colors[vehicle] = vehicle_color
        color_index += 1

        for route in vehicle.routes:
            previous_city = None
            for city in route:
                # Add node for each city with its geographical position
                G.add_node(city.name, pos=(city.lon, city.lat), label=f"{city.name} ({city.weight})")

                # Add edge if previous city exists
                if previous_city:
                    # Optionally, you can calculate the distance between cities to set as weight
                    G.add_edge(previous_city.name, city.name, color=vehicle_color)
                previous_city = city

    # Position nodes based on geographical coordinates
    pos = nx.get_node_attributes(G, 'pos')

    # Draw the graph
    # Draw nodes with positions
    nx.draw_networkx_nodes(G, pos)

    # Draw edges with different colors
    for edge in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])], edge_color=edge[2]['color'])

    # Draw labels
    nx.draw_networkx_labels(G, pos, {n: d['label'] for n, d in G.nodes(data=True)})

    # Create a legend for vehicles
    vehicle_legend = [plt.Line2D([0], [0], color=color, lw=4) for color in vehicle_colors.values()]
    plt.legend(vehicle_legend, [f"V: {v.number}" for v in vehicle_colors.keys()], loc='upper left')

    plt.axis('equal')  # Set equal scaling by x and y axes for correct geographical representation
    plt.show()




def generate_graph(orders_data, distance_matrix):
    """
    Creates a graph based on orders_data and distance matrix. Created graph
    will have all nodes connected in cartesian manner.
    """
    G = nx.Graph()
    for city in orders_data["city"]:
        row = orders_data[orders_data["city"] == city]
        location = (row["longitude"].iloc[0], row["latitude"].iloc[0])
        order = row["order"]
        G.add_node(city, location=location, order=order)

    for origin in orders_data["city"]:
        for destination in orders_data["city"]:
            if origin != destination:
                distance = distance_matrix.at[origin, destination]
                G.add_edge(origin, destination, distance=distance)

    return G


def generate_route_graphs(routes, orders_data, distance_matrix):
    """
    Creates a graph for a given route.
    """
    route_graphs = []
    for route in routes:
        RG = nx.Graph()
        prev_city = None
        for counter, city in enumerate(route):
            lon = orders_data[orders_data["city"] == city]["longitude"].iloc[0]
            lat = orders_data[orders_data["city"] == city]["latitude"].iloc[0]
            order = orders_data[orders_data["city"] == city]["order"].iloc[0]
            RG.add_node(city, pos=(lon, lat), stop=counter, order=order)
            if prev_city:
                distance = distance_matrix.at[city, prev_city]
                RG.add_edge(city, prev_city, weight=distance)
            prev_city = city
        route_graphs.append(RG)
    return route_graphs


def generate_graphs_depiction(route_graphs, depot="Kraków"):
    """
    Based on given nx.Graphs (list), generates a depiction for all routes.
    """
    plt.figure(figsize=(15, 10))

    # Define colors for different vehicles
    colors = [
        "red",
        "blue",
        "green",
        "yellow",
        "purple",
    ]  # Extend this list for more vehicles
    legend_elements = []

    for i, RG in enumerate(route_graphs):
        pos = nx.get_node_attributes(RG, "pos")

        # Create custom node labels, skipping labeling the depot with a stop number
        node_labels = {
            node: f"{node} (Stop: {RG.nodes[node]['stop']})" if node != depot else node
            for node in RG.nodes
        }

        # Draw nodes and edges for each vehicle
        nx.draw(
            RG,
            pos,
            labels=node_labels,
            with_labels=True,
            node_color="skyblue",
            node_size=500,
            edge_color=colors[i % len(colors)],
            width=2,
            alpha=0.6,
        )

        # Annotate edges with weights, formatted to two decimal places
        edge_labels = {
            edge: f"{weight:.2f}"
            for edge, weight in nx.get_edge_attributes(RG, "weight").items()
        }
        nx.draw_networkx_edge_labels(RG, pos, edge_labels=edge_labels, font_size=7)

        # Add legend element for this vehicle
        legend_elements.append(
            Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label=f"Vehicle {i+1}",
                markerfacecolor=colors[i % len(colors)],
                markersize=10,
            )
        )

    # Add legend for vehicle routes
    plt.legend(handles=legend_elements, loc="upper left")

    plt.title("Vehicle Routes with City Stops")
    plt.show()
