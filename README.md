# EntityTypeForKnowledgegraph
entity type inference

This project use the data, generated from the last project
after step 6: relation classification or clustering( map the text relation mention into the knowledge base relation), we can get a more dense relation schema(we reduce the relation number)

python getEnt2Type.py, we can get the data, then we copy the training data into this project data.

And then we can use the algorithm in paper [Inferring Missing Entity Type Instances for Knowledge Base Completion:
New Dataset and Methods]

we transfer type propagation problem into an type classification problem. Using the training data to get an type classifier.
