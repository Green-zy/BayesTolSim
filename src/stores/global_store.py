# src/stores/global_store.py

# Global storage dictionary for saving dimension data
dimensions_store = {}

def get_dimension(dim_key):
    """Get data for specified dimension"""
    return dimensions_store.get(dim_key)

def set_dimension(dim_key, data):
    """Set data for specified dimension"""
    dimensions_store[dim_key] = data

def update_dimension(dim_key, **kwargs):
    """Update partial data for specified dimension"""
    if dim_key not in dimensions_store:
        dimensions_store[dim_key] = {
            "name": f"Dim {dim_key.split('_')[1]}",
            "dist": None,
            "para1": None,
            "para2": None
        }
    
    for key, value in kwargs.items():
        dimensions_store[dim_key][key] = value

def remove_dimension(dim_key):
    """Remove specified dimension"""
    dimensions_store.pop(dim_key, None)

def clear_all_dimensions():
    """Clear all dimension data"""
    dimensions_store.clear()

def get_all_dimensions():
    """Get all dimension data"""
    return dimensions_store.copy()

def print_store_status():
    """Print current storage status (for debugging)"""
    print("Current dimensions_store:")
    for key, value in dimensions_store.items():
        print(f"  {key}: {value}")