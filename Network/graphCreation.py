import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def createGraph(edges,nodes):
    graph = nx.DiGraph()
    records = edges.to_records(index=False)
    result = list(records)
    graph.add_nodes_from(nodes.index)
    graph.add_edges_from(result)
    nx.set_node_attributes(graph, values=pd.Series(nodes.title, index=nodes.index).to_dict(), name='Title')
    nx.set_node_attributes(graph, values=pd.Series(nodes.year, index=nodes.index).to_dict(), name='Pubblication year')
    nx.set_node_attributes(graph, values=pd.Series(nodes.authors, index=nodes.index).to_dict(), name='Authors')
    nx.set_node_attributes(graph, values=pd.Series(nodes.source, index=nodes.index).to_dict(), name='Source Paper')
    nx.set_node_attributes(graph, values=pd.Series(nodes.doi, index=nodes.index).to_dict(), name='DOI')
    nx.set_node_attributes(graph, values=pd.Series(nodes.cit_score, index=nodes.index).to_dict(), name='Citation Score')
    return graph


def createFileCSV(nodes,edges):
    columns_name_nodes = ['id','label','authors','source_paper','year','doi','cit_score']
    columns_name_edges = ['source','target']

    nodes_gephi = pd.DataFrame(columns=columns_name_nodes)
    nodes_gephi['id'] = np.arange(1,len(nodes['title']),1,dtype=int)
    nodes_gephi['label'] = nodes['title']
    nodes_gephi['authors'] = nodes['authors']
    nodes_gephi['source_paper'] = nodes['source']
    nodes_gephi['year'] = nodes['year']
    nodes_gephi['doi'] = nodes['doi']
    nodes_gephi['cit_score'] = nodes['cit_score']
    nodes_gephi.set_index('id')

    nodes_gephi.to_csv('nodes.csv',sep='\t',index=False)
    
    edges_gephi = pd.DataFrame(columns=columns_name_edges)
    edges_gephi['source'] = edges['citing_pub_index']
    edges_gephi['target'] = edges['cited_pub_index']

    edges_gephi.to_csv('edges.csv',sep='\t',index=False)

    return nodes_gephi,edges_gephi

def find_n_top(n, graph, measure):
  count = 0
  for node in sorted(measure, key=measure.get, reverse=True):
    if count >= n:
      break
    print(f"Title:{graph.nodes[node]['Title']} - Value: {measure[node]}")
    count+=1


def computeMetrics(graph):
    print(nx.info(graph))
    print(f"Number of nodes: {nx.number_of_nodes(graph)}")
    print(f"Number of edges: {nx.number_of_edges(graph)}")

    print(f"Density: {nx.classes.function.density(graph)}")
    print(f"Reciprocity: {nx.reciprocity(graph)}")
    print(f"Transitivity: {nx.transitivity(graph)}")
    print(f"Average Clustering: {nx.average_clustering(graph)}")
    print(f"Edge Density: {nx.classes.function.density(graph)}")
  
    print(f"Average_Degree: {np.array([d for n, d in graph.degree()]).sum()/nx.number_of_nodes(graph)}")

    degree_centrality = nx.degree_centrality(graph)
    print(f"Degree centrality: {np.mean(list(degree_centrality))}")

    #Top 5 nodes as betweenness centrality 
    print("Top 5 nodes as betweenness centrality")
    bet_centr_unw_und = nx.betweenness_centrality(graph)
    find_n_top(5,graph,bet_centr_unw_und)


    degrees = [graph.in_degree(n) for n in graph.nodes()]
    plt.hist(degrees)
    plt.title("Degree Histogram")
    plt.savefig("images/hist_Degree-png")
    plt.show()

    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    plt.loglog(degree_sequence,marker='*')
    plt.title("Degree Sequence")
    plt.savefig("images/degree_seq.png")
    plt.show()
 


if __name__ == '__main__':
  nodes = pd.read_csv('data/pubblications.txt',sep='\t') 
  edges = pd.read_csv('data/citations.txt',sep='\t')

  citation_network = createGraph(edges,nodes)

  #Create .csv file for gephi
  #createFileCSV(nodes,edges)
  
  computeMetrics(citation_network)
