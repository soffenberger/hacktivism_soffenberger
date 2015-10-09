import networkx as nx
import psycopg2 as ps
import matplotlib.pyplot as plt

   



class user_graph(object):
	
	def __init__(self):
		self.graph = nx.Graph()
		self.edges = []
		self.nodes = []
			

	def add_nodes(self, edges, nodes):			
		self.edges = edges			
		self.nodes = nodes
		with open ('file.txt', 'w') as data:
			for i in self.edges:
				data.write(str(i) + '\n')

	def add_user_nodes(self):
		#try:
		self.graph.add_nodes_from(self.nodes)
		#except ValueError:
		#	print "IDK"

	def add_user_edges(self):
		self.graph.add_edges_from(self.edges)

		#except ValueError:
		#	print "IDK"

	def add_characteristic(self, jk, ff, date):
		self.graph.edge[jk][ff]['date'] = date

	def print_graph(self):
		nx.write_graphml(self.graph,'so.graphml')			


if __name__ == '__main()__':
	self()
