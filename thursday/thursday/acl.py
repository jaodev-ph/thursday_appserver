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
    'tenants': {
        'name': 'Tenants',
        'parent_id': 'root',
        'possible_privileges': [0, 1, 2, 3, 4],
        'icon': 'mdi mdi-domain',
        'default': ACL_INHERITED,
        'sort': 20
    },
    'users': {
        'name': 'Users',
        'parent_id': 'root',
        'possible_privileges': [0, 1, 2, 3, 4],
        'icon': 'mdi mdi-account-group',
        'default': ACL_INHERITED,
        'sort': 30
    },
    'bots': {
        'name': 'Bots',
        'parent_id': 'root',
        'possible_privileges': [0, 1, 2, 3, 4],
        'icon': 'mdi mdi-robot',
        'default': ACL_INHERITED,
        'sort': 40
    },
    'conversations': {
        'name': 'Conversations',
        'parent_id': 'root',
        'possible_privileges': [0, 1, 2, 3, 4],
        'icon': 'mdi mdi-chat',
        'default': ACL_INHERITED,
        'sort': 50
    },
    'customers': {
        'name': 'Customers',
        'parent_id': 'root',
        'possible_privileges': [0, 1, 2, 3, 4],
        'icon': 'mdi mdi-account',
        'default': ACL_INHERITED,
        'sort': 60
    },
    'messages': {
        'name': 'Messages',
        'parent_id': 'root',
        'possible_privileges': [0, 1, 2, 3, 4],
        'icon': 'mdi mdi-message',
        'default': ACL_INHERITED,
        'sort': 70
    },
    'settings': {
        'name': 'Settings',
        'parent_id': 'root',
        'possible_privileges': [0, 1, 2, 3, 4],
        'icon': 'mdi mdi-cog',
        'default': ACL_INHERITED,
        'sort': 80
    }
}

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