def to_dropdown_option(keys:list,values:list)-> list(tuple):
    if not isinstance(keys,list):
        raise TypeError
    if not isinstance(values,list):
        raise TypeError

    return list(zip(keys,values))