import DAG

if __name__ == '__main__':
    # Default if only a node is provided is FullTree: False, Visualization: False
    DAG.build_dag('Person', False, True)
