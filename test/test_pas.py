from src.pas import tree_splitter, edge_counter, totalEdgeCount, internalCount, leafCount

node_dict = {'tree':'(bob{1},bill|c|{3})'
}

def test_tree_splitter():
    print(tree_splitter(node_dict))
    assert tree_splitter(node_dict) == ['','1|b|','2|c|{3}','']

def test_edge_counter():
    edge_counter(node_dict)
    print(edge_counter(node_dict))
    assert totalEdgeCount == 2
    assert leafCount == 1
    assert internalCount == 1
    assert leafEdges == 1
 #   assert internalEdges ==


