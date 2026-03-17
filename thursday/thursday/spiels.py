GENERIC_SPIEL = {
    'create': {
        'success': lambda module="tenant": f"{module.capitalize()} created successfully",
        'error': lambda module="tenant", name=None: f"Error creating {module}{f' \"{name}\"' if name else ''}",
    },
    'delete': {
        'success': lambda module="tenant", name=None: f"{module.capitalize()}{f' \"{name}\"' if name else ''} deleted successfully",
        'error': lambda module="tenant", name=None: f"Error deleting {module}{f' \"{name}\"' if name else ''}",
    },
    'update': {
        'success': lambda module="tenant", name=None: f"{module.capitalize()}{f' \"{name}\"' if name else ''} updated successfully",
        'error': lambda module="tenant", name=None: f"Error updating {module}{f' \"{name}\"' if name else ''}",
    },
    'get': {
        'success': lambda module="tenant", name=None: f"{module.capitalize()}{f' \"{name}\"' if name else ''} retrieved successfully",
        'error': lambda module="tenant", name=None: f"Error retrieving {module}{f' \"{name}\"' if name else ''}",
    },
}