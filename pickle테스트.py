import pickle

with open('ai_domain.pickle', 'rb') as f:
    my_list = pickle.load( f)

print(my_list)