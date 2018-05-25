#!/usr/bin/env python

# This is an automatically generated script to run your query
# to use it you will require the intermine python client.
# To install the client, run the following command from a terminal:
#
#     sudo easy_install intermine
#
# For further documentation you can visit:
#     http://intermine.readthedocs.org/en/latest/web-services/

# The following two lines will be needed in every python script:
from intermine.webservice import Service
service = Service("https://phytozome.jgi.doe.gov/phytomine/service")

# Get a new query on the class (table) you will be querying:
query = service.new_query("Gene")

# The view specifies the output columns
query.add_view(
    "name", "primaryIdentifier", "secondaryIdentifier", "length",
    "flankingRegions.length", "flankingRegions.includeGene",
    "flankingRegions.direction", "flankingRegions.primaryIdentifier",
    "flankingRegions.sequence.length", "flankingRegions.sequence.residues"
)

# Uncomment and edit the line below (the default) to select a custom sort order:
# query.add_sort_order("Gene.name", "ASC")

# You can edit the constraint values below
query.add_constraint("flankingRegions.length", "=", "5000", code = "A")
query.add_constraint("flankingRegions.includeGene", "=", "false", code = "B")
query.add_constraint("flankingRegions.direction", "=", "upstream", code = "C")
query.add_constraint("name", "=", "Vigun03g422000", code = "D")

# Uncomment and edit the code below to specify your own custom logic:
# query.set_logic("A and B and C and E")

for row in query.rows():
    print (row["name"], row["primaryIdentifier"], row["secondaryIdentifier"], row["length"], \
        row["flankingRegions.length"], row["flankingRegions.includeGene"], \
        row["flankingRegions.direction"], row["flankingRegions.primaryIdentifier"], \
        row["flankingRegions.sequence.length"], row["flankingRegions.sequence.residues"])

