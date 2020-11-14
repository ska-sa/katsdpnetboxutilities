import logging
import os

from collections import defaultdict

from graphviz import Graph


def extract_components_from_netbox_result(dataset, config):
    edges = []
    nodes = []
    records = defaultdict(dict)
    subgraphs = defaultdict(dict)
    for link in dataset:
        logging.debug("link: %s", link)
        # Create the internal references
        device_a = "d{}".format(link["interface_a"]["device"]["id"])
        intf_a = "i{}".format(link["interface_a"]["id"])
        device_b = "d{}".format(link["interface_b"]["device"]["id"])
        intf_b = "i{}".format(link["interface_b"]["id"])
        if config["subgraph"]:
            subgraphs[device_a]["_info"] = link["interface_a"]["device"]
            subgraphs[device_b]["_info"] = link["interface_b"]["device"]
            subgraphs[device_a][intf_a] = link["interface_a"]
            subgraphs[device_b][intf_b] = link["interface_b"]
        else:
            records[device_a]["_info"] = link["interface_a"]["device"]
            records[device_b]["_info"] = link["interface_b"]["device"]
            records[device_a][intf_a] = link["interface_a"]
            records[device_b][intf_b] = link["interface_b"]
            intf_a = "{}:{}".format(device_a, intf_a)
            intf_b = "{}:{}".format(device_b, intf_b)
        edges.append({"a": intf_a, "b": intf_b})
    return {"edges": edges, "nodes": nodes, "subgraphs": subgraphs, "records": records}


def add_edges(graph, edges):
    for edge in edges:
        graph.edge(edge["a"], edge["b"])


def add_nodes(graph, nodes):
    pass


def add_records(graph, records):
    for record_name, record in records.items():
        label = "{}".format(record["_info"]["name"])
        for intf_name, intf in record.items():
            if not intf_name.startswith("_"):
                label += "|<{}> {}".format(intf_name, intf["name"])
        graph.node(name=record_name, shape="record", label=label, url=intf["url"])


def add_subgraphs(graph, subgraphs):
    for subgraph_name, subgraph in subgraphs.items():
        with graph.subgraph(name="cluster_" + subgraph_name) as subg:
            subg.attr(label=subgraph["_info"]["name"])
            subg.attr(color="blue")
            for intf_name, intf in subgraph.items():
                if not intf_name.startswith("_"):
                    subg.node(
                        name=intf_name, shape="box", label=intf["name"], url=intf["url"]
                    )


def create_graphviz(components, config):
    graph = Graph(
        name=config["name"], engine=config["engine"], directory=config["output_path"]
    )
    if config.get("horizontal"):
        rankdir = "TB"
    else:
        rankdir = "LR"
    graph.attr(rankdir="LR", overlap="false")

    add_subgraphs(graph, components["subgraphs"])
    add_records(graph, components["records"])
    add_nodes(graph, components["nodes"])
    add_edges(graph, components["edges"])

    return graph


def make_dot_file(config, dataset):
    components = extract_components_from_netbox_result(dataset, config)
    graph = create_graphviz(components, config)
    filename = config["name"] + ".gv"
    graph.save(directory=config["output_path"], filename=filename)
    graph.render(
        directory=config["output_path"],
        filename=filename,
        view=config["live"],
        format=config["format"],
    )
