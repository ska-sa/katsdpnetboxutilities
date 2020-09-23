import logging
import os

from collections import defaultdict

from graphviz import Graph


def extract_edges_subgraphs_from_netbox_result(dataset):
    edges = []
    subgraphs = defaultdict(dict)
    for link in dataset:
        logging.debug("link: %s", link)
        # Create the internal references
        device_a = "d{}".format(link["interface_a"]["device"]["id"])
        intf_a = "i{}".format(link["interface_a"]["id"])
        device_b = "d{}".format(link["interface_b"]["device"]["id"])
        intf_b = "i{}".format(link["interface_b"]["id"])
        subgraphs[device_a]["_info"] = link["interface_a"]["device"]
        subgraphs[device_b]["_info"] = link["interface_b"]["device"]
        subgraphs[device_a][intf_a] = link["interface_a"]
        subgraphs[device_b][intf_b] = link["interface_b"]
        edges.append({"a": intf_a, "b": intf_b})
    return edges, subgraphs


def create_graphviz(edges, subgraphs):
    graph = Graph(name="sarao")
    graph.attr(rankdir='LR', overlap='false')
    for subgraph_name, subgraph in subgraphs.items():
        with graph.subgraph(name="cluster_" + subgraph_name) as subg:
            subg.attr(label=subgraph["_info"]["name"])
            subg.attr(color="blue")
            for intf_name, intf in subgraph.items():
                if not intf_name.startswith("_"):
                    subg.node(
                        name=intf_name, shape="box", label=intf["name"], url=intf["url"]
                    )

    for edge in edges:
        graph.edge(edge["a"], edge["b"])

    return graph


def make_dot_file(config, dataset):
    edges, subgraphs = extract_edges_subgraphs_from_netbox_result(dataset)
    graph = create_graphviz(edges, subgraphs)
    filename = config["name"] + ".gv"
    graph.save(directory=config["output_path"], filename=filename)
    graph.render(
        directory=config["output_path"],
        filename=filename,
        view=config["live"],
        format="pdf",
    )
