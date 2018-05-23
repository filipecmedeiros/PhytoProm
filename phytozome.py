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
    "flankingRegions.length", "flankingRegions.includeGene",
    "flankingRegions.primaryIdentifier", "flankingRegions.direction"
)

# This query's custom sort order is specified below:
query.add_sort_order("Gene.flankingRegions.primaryIdentifier", "ASC")

# You can edit the constraint values below
query.add_constraint("flankingRegions.length", "ONE OF", ["5000"], code = "A")
query.add_constraint("flankingRegions.includeGene", "=", "false", code = "B")
query.add_constraint("flankingRegions.primaryIdentifier", "CONTAINS", "Vigun", code = "C")
query.add_constraint("flankingRegions.direction", "ONE OF", ["upstream"], code = "D")


# Uncomment and edit the code below to specify your own custom logic:
query.set_logic("A and B and C and D")

i=
for row in query.rows():

    print (row["flankingRegions.length"], row["flankingRegions.includeGene"], \
        row["flankingRegions.primaryIdentifier"], row["flankingRegions.direction"])
