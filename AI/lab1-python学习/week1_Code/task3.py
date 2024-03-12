def ReverseKeyValue(dict1):
    """
    :param dict1: dict
    :return: dict
    """
    dict2={}
    for name,num in dict1.items():
        dict2[num]=name
    return dict2
dict1={'Alice':'001', 'Bob':'002'}
print(ReverseKeyValue(dict1))
       
 