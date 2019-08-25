# Builds URL
def build_url(path):
    return '/'.join(path)

# Constructs a get request string given a dict of params and a base url
def construct_request_string(base_url, params):
    string = "{}?".format(base_url)
    params_arr = []
    for key, value in params.items():
        params_arr.append("{}={}".format(key, value.replace(' ', '%20')))
    string += '&'.join(params_arr)
    return string

# Checks for error status codes
def successful_request(request_json):
    if request_json['error']:
        return False
    else:
        return True