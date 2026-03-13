from common.acl import ACL, ACL_INHERITED, ACL_NO_ACCESS, ACL_VIEW, ACL_MODIFY, ACL_ADD_DELETE

auth_objects = {
    'root': {
        'name': 'All Menu', 
        'parent_id': None, 
        'possible_privileges': [1, 2, 3, 4], 
        'default': ACL_INHERITED, 
        'sort': 1
    },
    'dashboard': {
        'name': 'Dashboard',
        'parent_id': 'root',
        'possible_privileges': [0, 1, 2, 3, 4], 
        'icon': 'mdi mdi-chart-arc', 
        'default': ACL_INHERITED, 
        'sort': 10
    },
}


def get_jstree_parsed():
    data = []
    for key, val in auth_objects.items():
        data.append({
            'id': key,
            'parent': '#' if val['parent_id'] is None else val['parent_id'],
            'text': val.get('name'),
            'state': {'opened': 'true'},
            'icon': val.get('icon', 'mdi mdi-file'),
            'possible_privileges': val['possible_privileges']
        })
    return { 'core': {'data': data}, 'themes': { 'name' : 'default' } }


def get_admin_acl():
	output = {}
	for key, val in auth_objects.items():
		output[key] = 4 #- ACL_ADD_DELETE
	return output

def get_public_acl():
	return {key: 2 if key in ['map'] else 1 for key, value in auth_objects.items()}

def page_has_no_access(user_privileges, current_page):
	if current_page in auth_objects:
		return user_privileges[current_page] < 2  #ACL_VIEW = 2
	else:
		return True

def get_free_tier():
    output = {}
    acl_obj = ACL(auth_objects, {})
    for key, val in auth_objects.items():
        output[key] = acl_obj.setDefaultPrivilege(key)
    return output