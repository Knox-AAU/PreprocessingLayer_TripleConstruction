from rdflib import Graph, URIRef, Literal
from rdflib.plugins.sparql import prepareQuery

# Load your ontology
g = Graph()
g.parse("ontology.ttl", format="turtle")  # Replace with the actual path to your ontology file

# Define the SPARQL query
query = prepareQuery(
    """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://dbpedia.org/ontology/>

SELECT DISTINCT ?subClass
WHERE {
    ?subClass rdfs:subClassOf* :Organisation .
}

    """
)

# Execute the query
results = g.query(query)

# Print the results
for row in results:
    # Use n3() to print the class name
    print(row.subClass.n3().removeprefix('<http://dbpedia.org/ontology/').removesuffix('>'))