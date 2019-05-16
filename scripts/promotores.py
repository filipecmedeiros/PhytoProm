import numpy as np
import pandas as pd

arquivo = 'Mitalle'

df = pd.read_csv(
    arquivo + '.txt',
    sep=',', header=None, names=['id'])

from intermine.webservice import Service
service = Service("https://phytozome.jgi.doe.gov/phytomine/service")

query = service.new_query("Gene")

query.add_view(
    "name", "primaryIdentifier", "secondaryIdentifier", "length",
    "flankingRegions.length", "flankingRegions.includeGene",
    "flankingRegions.direction", "flankingRegions.primaryIdentifier",
    "flankingRegions.sequence.length", "flankingRegions.sequence.residues"
)

query.add_constraint("flankingRegions.length", "=", "5000", code = "A")
query.add_constraint("flankingRegions.includeGene", "=", "false", code = "B")
query.add_constraint("flankingRegions.direction", "=", "upstream", code = "C")

with open (arquivo+".fas", "w") as promotores:
    for i in df['id']:
        query.add_constraint("name", "=", i, code = "D")
        for row in query.rows():
            promotores.write(">"+str(row["primaryIdentifier"])+'\n'+\
                            str(row["flankingRegions.sequence.residues"][4000:])+'\n') #Salvar apenas as ultimas 2000 bases