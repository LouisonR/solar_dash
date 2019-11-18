
def build_options(site_access_lst):
    """ Returns an option list.

    Parameters:
        site_access_lst (list): list of tuple (site_id, site_name)

    Returns:
        options_list (list): list of dict {'label', 'value'}

    """
    options_lst = []
    for site_id, site_name in site_access_lst:
        options_lst.append({'label': site_name, 'value': site_id})
    return options_lst


def get_name(tab_lst, elt_id, default):
    """ Returns a name.

    Parameters:
        tab_lst (list): list of tuple (id, name)
        elt_id (int): look for the name of the elt_id
        default (string): default value if elt_id not found in tab_lst

    Returns:
        name (string): name found in the tab_lst

    """
    name = default
    for elt in tab_lst:
        if elt_id == elt[0]:
            name = elt[1]
    return name
