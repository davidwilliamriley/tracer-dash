

class Edge_Controller:
    def __init__(self, model):
        self.model = model

    def get_edges(self):
        return self.model.get_edges()

    def create_edge(self, edge_data):
        return self.model.create_edge(edge_data)

    def update_edge(self, edge_id, edge_data):
        return self.model.update_edge(edge_id, edge_data)

    def delete_edge(self, edge_id):
        return self.model.delete_edge(edge_id)