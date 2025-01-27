import blueprint.bphandler as bphandler
import blueprint.filehandler as filehandler
import blueprint.out as out

import mesh.objhandler as objhandler

import json

def importer(obj: str, compartment: str, asVehicle: str = "", thickness = 1) -> str:
    """
    Import .obj string as sprocket compartment or into vehicle if asVehicle is specified

    asVehicle should be a string containing data of the file.
    """
    # TODO: implement compartment-only generation
    if asVehicle != "":
        vData = json.loads(asVehicle)
        
        scene = objhandler.load_shape_from_obj(obj)
        vertices = objhandler.populate_vertices_alt(scene)
        faces = objhandler.populate_faces_alt(scene, thickness=thickness)

        vertices, faces = objhandler.merge_duplicate_points(vertices, faces)

        vertices = out.reformat_vertices(vertices)
        faces = out.reformat_faces(faces)

        vuid = bphandler.get_vuid(vData, compartment)

        template = out.fill_template(vuid, vertices, faces)[0]

        cData = {
            'meshes': [template]
        }

        found = False

        for mesh in vData['meshes']:
            print(f'{mesh["vuid"]=}')
            if mesh['vuid'] == vuid:
                mesh['meshData']['mesh'] = cData['meshes'][0]['meshData']['mesh']
                found = True
                
        if not found:
            err = 3
            return (f"Compartment <{compartment}> not found. Aborting with error code {err}.", err)

        return ("vData", 0)

if __name__ == "__main__":
    print(importer()[0])