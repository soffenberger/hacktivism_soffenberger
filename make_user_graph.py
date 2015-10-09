import create_user_graph as cp
import psycopg2	as ps
from datetime import timedelta, date
import sys

def get_list_of_users():
	conn = ps.connect("dbname = 'hacktivism'")
	cur = conn.cursor()
	cur.execute("select screen_name,user_mentions from {0};".format(sys.argv[1]))
	users = cur.fetchall()
	temp_tuple = ()
	temp_tuple1 = ()
	edges = []
	nodes = []
	for i in users:
		str_list = i[1].split(',')
		str_list = filter(None, str_list)
		#print (i[0], )+tuple(str_list), len(str_list)
		if len(str_list) == 1:
			temp_tuple = (i[0], ) + tuple(str_list)
			edges.append(temp_tuple)
			nodes.extend([i[0],str_list[0]])
		elif len(str_list) ==2:
			temp_tuple = (i[0],str_list[0])
			temp_tuple1 = (i[0], str_list[1])
			edges.extend([temp_tuple, temp_tuple1])
			nodes.extend([i[0],str_list[0],str_list[1]])
		elif len(str_list) ==3:

			temp_tuple = (i[0], str_list[0])
			temp_tuple2 = (i[0], str_list[1])
			temp_tuple1 = (i[0], str_list[2])
			edges.extend([temp_tuple, temp_tuple1, temp_tuple2])
			nodes.extend([i[0],str_list[0],str_list[1], str_list[2]])

		#elif len(str_list) ==4:
		#	temp_tuple = (i[0],) + tuple(str_list[:2])
		#	temp_tuple1 = (i[0],) + tuple(str_list[2:])
		#	edges.extend([temp_tuple, temp_tuple1] )
		#	nodes.extend([i[0],str_list[0],str_list[1], str_list[2], str_list[3]])
		else:
			nodes.append(i[0])
	conn.commit()
	cur.close()
	conn.close()
	return nodes,edges
	
	

def create_graph():
	nodes,edges = get_list_of_users()
	user_graph = cp.user_graph()
	#user_graph.add_nodes(nodes)
	user_graph.edges.extend(edges)
	user_graph.nodes.extend(nodes)
	with open ('file1.txt', 'w') as data:
			for i in user_graph.edges:
				data.write(str(i) + '\n')
	user_graph.add_user_nodes()
	user_graph.add_user_edges()
	conn = ps.connect("dbname = 'hacktivism'")
	cur = conn.cursor()
	for i in edges:
		cur.execute("""select created_time from {0} where screen_name = '{1}' and user_mentions like '%{2}%'; """.format(sys.argv[1], i[0], i[1]))
		time = cur.fetchone()
		print time[0].strftime('%m/%d/%Y')
		user_graph.add_characteristic(i[0], i[1], time[0].strftime('%m/%d/%Y'))
	user_graph.print_graph()
	conn.commit()
	cur.close()
	conn.close()
def main():
	create_graph()
	
	

if __name__ == "__main__":
	main()
