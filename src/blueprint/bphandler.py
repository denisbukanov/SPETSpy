

def get_vuid(data: dict, partName: str) -> int | None:
    """
    Get vuid given part name
    """
    vuid = None
    for bp in data['blueprints']:
        print(f'{bp["blueprint"]["name"]=}')
        if bp['blueprint']['name'] == partName:
            print('Found')
            vuid = bp['blueprint']['bodyMeshVuid']

    return vuid
