def extract_specific_relations(ontology_file_path):
    "Function to extract relations based on the specified pattern"
    relations = set()
    with open(ontology_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        i = 0
        for i, line in enumerate(lines):
            line = line.strip()
            # Check if the line starts with a colon and the next lines contain the specified pattern
            if line.startswith(":") and i+1 < len(lines) and "a rdf:Property, owl:ObjectProperty ;" in lines[i+1]:
                relation = line.split()[0]  # Extracting the relation name
                relation = relation[1:] # Remove colon
                relations.add(relation)
            i += 1
            
    return sorted(relations) 