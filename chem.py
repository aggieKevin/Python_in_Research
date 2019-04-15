# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 10:06:45 2019

@author: hejia
"""

import pandas as pd
import numpy as np
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_colwidth',100)
pd.set_option('display.width',None)

def check_smiles(smiles):
    smiles_after_strip=smiles.strip('[').strip(']')
    smiles_seperate=smiles_after_strip.split(',')
    return smiles_seperate[0]

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit.Chem.AtomPairs import Pairs

def caculate_similarity_fingerprint(smiles_A,smiles_B):
    try:
        m1=Chem.MolFromSmiles(smiles_A)
        m2=Chem.MolFromSmiles(smiles_B)
        f1=FingerprintMols.FingerprintMol(m1)
        f2=FingerprintMols.FingerprintMol(m2)
        
        similaritt_f1_f2=DataStructs.FingerprintSimilarity(f1,f2)
        return round(similaritt_f1_f2,4)
    except:
        return -1
def caculate_similarity_atomPairs(smiles_A,smiles_B):
    try:
        m1=Chem.MolFromSmiles(smiles_A)
        m2=Chem.MolFromSmiles(smiles_B)
        p1=Pairs.GetAtomPairFingerprint(m1)
        p2=Pairs.GetAtomPairFingerprint(m2)      
        similarity_p1_p2=DataStructs.DiceSimilarity(p1,p2)
        return round(similarity_p1_p2,4)
    except:
        return -1


file=pd.read_csv('C:\\Users\\hejia\\Documents\\BasicDrugOverview.csv',index_col='drugid',encoding='latin-1')
drug_smiles=file['structuresmiles'].dropna()

columns=['drupid_A','drugid_B','fingerprint_similarity','atomPairs_similarity']
df_similarity= pd.DataFrame(columns=columns)

drug_smiles_100=drug_smiles[0:100]
for i in drug_smiles_100.index:
    if ',' in drug_smiles_100.loc[i]:
        drug_smiles_100.loc[i]=check_smiles(drug_smiles_100.loc[i])
INDEX=0
for i in drug_smiles_100.index:
    print('i is ',i)
    for j in drug_smiles_100.index:
        print('j is ,',j)
        smiles_A=drug_smiles_100.loc[i]
        smiles_B=drug_smiles_100.loc[j]       
        print(caculate_similarity_fingerprint(smiles_A,smiles_B))
        print(caculate_similarity_atomPairs(smiles_A,smiles_B))       
        df_similarity.loc[INDEX]=[int(i),int(j),caculate_similarity_fingerprint(smiles_A,smiles_B),caculate_similarity_atomPairs(smiles_A,smiles_B)]
        INDEX+=1
df_similarity.to_csv('C:\\Users\\hejia\\Dropbox\\Dr Wu\\df_similarity.csv')   

        
        
        



    
    
    
'''

for i in range(100):
    for j in range(100):
        
    
from rdkit import Chem
mol = Chem.MolFromSmiles('[C@H](Cl)(F)Br')
from rdkit.Chem import AllChem
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols

smile1='Cn1c(ccn1)c2c3ccccc3c(nn2)N4CCC(CC4)N(C)C(=O)c5ccc(cc5C(F)(F)F)F'
smile2='Cn1ncc(c1)c2c3c(ncc(c3)[C@H]4CC[C@@H](CC4)N5CCOCC5)[nH]c2'
m1=Chem.MolFromSmiles(smile1)
m2=Chem.MolFromSmiles(smile2)
#m1=Chem.MolFromSmiles('CCOC')
#m2=Chem.MolFromSmiles('CCO')
#m3=Chem.MolFromSmiles('COC')
f1=FingerprintMols.FingerprintMol(m1)
f2=FingerprintMols.FingerprintMol(m2)
#f3=FingerprintMols.FingerprintMol(m3)
sim12=DataStructs.FingerprintSimilarity(f1,f2)

print(sim12)

Chem.Draw.MolToImage(m1,size=(700, 700))
Chem.Draw.MolToImage(m2,size=(700, 700))

from rdkit.Chem.AtomPairs import Pairs


p1=Pairs.GetAtomPairFingerprint(smile1)
p2=Pairs.GetAtomPairFingerprintAsBitVect(smile2)
from rdkit import DataStructs
DataStructs.DiceSimilarity(p1,p2)


from rdkit.Chem.AtomPairs import Pairs
ms = [Chem.MolFromSmiles('C1CCC1OCC'),Chem.MolFromSmiles('CC(C)OCC'),Chem.MolFromSmiles('CCOCC')]
pairFps = [Pairs.GetAtomPairFingerprint(x) for x in ms]
p12=DataStructs.DiceSimilarity(pairFps[0],pairFps[1])
print(p12)

'''




