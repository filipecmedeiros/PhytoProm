
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


ft = pd.read_csv(
    'transcriptors_matrix.txt',
    sep=',', header=None, names=['id', 'family', 'A', 'C', 'G', 'T'])
print(type(ft), ft.shape)
ft


# In[3]:


print(ft['A'][0])
print(ft['C'][0])
print(ft['G'][0])
print (ft['T'][0])


# In[4]:


def f_str_list (string):
    string = string.split()
    listed = []
    i = 2
    while(string[i] != ']'):
            listed.append(int (string[i]))
            i +=1
    
    return listed


# In[5]:


ft['A'][0].split()


# In[6]:


np_grupo_a = ft['A']


# In[7]:


np_grupo_a.count()


# In[8]:


i=0
while (i<489):
    np_grupo_a[i] = f_str_list(np_grupo_a[i])
    i += 1


# In[9]:


np_grupo_a


# In[10]:


type(np_grupo_a[0][0])


# In[11]:


ft['A'] = np_grupo_a


# In[12]:


ft['A']


# In[13]:


np_grupo_c = ft['C']


# In[14]:


i=0
while (i<489):
    np_grupo_c[i] = f_str_list(np_grupo_c[i])
    i += 1


# In[15]:


ft['C'] = np_grupo_c


# In[16]:


ft['C']


# In[17]:


np_grupo_g = ft['G']


# In[18]:


i=0
while (i<489):
    np_grupo_g[i] = f_str_list(np_grupo_g[i])
    i += 1


# In[19]:


ft['G'] = np_grupo_g


# In[20]:


np_grupo_t = ft['T']


# In[21]:


i=0
while (i<489):
    np_grupo_t[i] = f_str_list(np_grupo_t[i])
    i += 1


# In[22]:


ft['T'] = np_grupo_t


# In[23]:


ft


# In[24]:


ft['A'][0][0]

