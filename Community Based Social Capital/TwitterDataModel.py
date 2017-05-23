class Node:
    def __init__(self, id):
        self.id=id

    def get_id(self):
        return self.id

class Edge:
    def __init__(self, source, dest):
        self.source=source
        self.dest=dest

    def get_source(self):
        return self.source

    def get_dest(self):
        return self.dest


class Graph:
    def __init__(self):
        self.nodes=[]
        self.edges={}

    def add_edge(self, new_edge):
        if (self.nodes).count(new_edge.get_source()) == 0:
            self.nodes.append(new_edge.get_source())
        if (self.nodes).count(new_edge.get_dest()) == 0:
            self.nodes.append(new_edge.get_dest())

    def add_node(self, new_node):
        if (self.nodes).count(new_node) == 0:
            self.nodes.append(new_node)