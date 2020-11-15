import logging
import os
import json

from pathlib import Path
from collections import defaultdict

from graphviz import Graph


class ParseNetboxResults:
    def __init__(self, config):
        self.config = config
        self.edges = []
        self.nodes = []
        self.records = defaultdict(dict)
        self.subgraphs = defaultdict(dict)
        self.wpath = None

    def add_working_directory(self, path):
        self.wpath = Path(path)
        for filename in self.wpath.glob("connection+*"):
            self.add_connection_file(filename)

    def add_query_results(self, dataset):
        for link in dataset:
            self.add_connection(link)

    def add_connection(self, link):
        logging.debug("link: %s", link)
        # Create the internal references
        device_a = "d{}".format(link["interface_a"]["device"]["id"])
        intf_a = "i{}".format(link["interface_a"]["id"])
        device_b = "d{}".format(link["interface_b"]["device"]["id"])
        intf_b = "i{}".format(link["interface_b"]["id"])
        if self.config["subgraph"]:
            self.subgraphs[device_a]["_info"] = link["interface_a"]["device"]
            self.subgraphs[device_b]["_info"] = link["interface_b"]["device"]
            self.subgraphs[device_a][intf_a] = link["interface_a"]
            self.subgraphs[device_b][intf_b] = link["interface_b"]
        else:
            self.records[device_a]["_info"] = link["interface_a"]["device"]
            self.records[device_b]["_info"] = link["interface_b"]["device"]
            self.records[device_a][intf_a] = link["interface_a"]
            self.records[device_b][intf_b] = link["interface_b"]
            intf_a = "{}:{}".format(device_a, intf_a)
            intf_b = "{}:{}".format(device_b, intf_b)
        self.edges.append({"a": intf_a, "b": intf_b})

    def add_connection_file(self, filename):
        filename = Path(filename)
        if filename.exists():
            with filename.open() as plfile:
                self.add_connection(json.load(plfile))


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

    add_subgraphs(graph, components.subgraphs)
    add_records(graph, components.records)
    add_nodes(graph, components.nodes)
    add_edges(graph, components.edges)

    return graph


def make_dot_file(config, dataset):
    netbox_results = ParseNetboxResults(config)
    netbox_results.add_query_results(dataset)
    graph = create_graphviz(netbox_results, config)
    filename = config["name"] + ".gv"
    graph.save(directory=config["output_path"], filename=filename)
    graph.render(
        directory=config["output_path"],
        filename=filename,
        view=config["live"],
        format=config["format"],
    )


def make_dot_file_from_path(config):
    path = config["working_path"]
    netbox_results = ParseNetboxResults(config)
    netbox_results.add_working_directory(path)
    graph = create_graphviz(netbox_results, config)
    filename = config["name"] + ".gv"
    graph.save(directory=config["output_path"], filename=filename)
    graph.render(
        directory=config["output_path"],
        filename=filename,
        view=config["live"],
        format=config["format"],
    )
