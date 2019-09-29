# Builds URL
def build_url(*args):
    return '/'.join(args)

# Constructs a get request string given a dict of params and a base url
def construct_request_string(base_url, params):
    string = "{}?".format(base_url)
    params_arr = []
    for key, value in params.items():
        params_arr.append("{}={}".format(key, value.replace(' ', '%20')))
    string += '&'.join(params_arr)
    return string

# Helper method - filters response json to only include keys of interest
# In keys_of_interest, keys multiple levels deep can be specified using : (example: key1:key2:...)
def filter_dict(full_dict, keys_of_interest):
    filtered_dict = {}
    for key in keys_of_interest:
        # Handle keys multiple levels deep
        nested_keys = key.split(':')
        key_name = '_'.join(nested_keys)
        val = full_dict
        for k in nested_keys:
            val = val[k]
        filtered_dict[key_name] = val
    return filtered_dict