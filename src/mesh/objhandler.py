import pywavefront as pwf
import sprocketlib as spl
import copy

def create_scene(filepath: str) -> pwf.Wavefront:
    """
    Create a PyWaveFront Scene
    """
    scene = pwf.Wavefront(
        filepath,
        create_materials=True,
        collect_faces=True,
    )
    scene.parse()
    return scene

def load_shape_from_obj(data, raw = True):
    if not raw:
        vertices = []
        faces = []
        with open(data) as f:
            for line in f:
                if line[0:2] == "v ":
                    vertex = list(map(float, line[2:].strip().split()))
                    vertices.append(vertex)
                elif line[0] == "f":
                    face = []
                    for i in line[2:].strip().split():
                        face.append(int(i.split('/')[0]))
                    for i in range(len(face)):
                        face[i] = face[i] - 1

                    faces.append(face)

        shape_data = {"vertices": vertices, "faces": faces}

        return shape_data
    vertices = []
    faces = []
    for line in data:
        if line[0:2] == "v ":
            vertex = list(map(float, line[2:].strip().split()))
            vertices.append(vertex)
        elif line[0] == "f":
            face = list(map(int, line[2:].strip().split()))
            faces.append(face)

    shape_data = {"vertices": vertices, "faces": faces}

    return shape_data

def populate_vertices(scene: pwf.Wavefront) -> list[spl.mesh.Vertex]:
    """
    Create a list of sprocketlib.mesh.Vertex objects
    """
    vertices = []
    index = 0
    for i in scene.vertices:
        vertices.append(spl.mesh.Vertex( i[0] , i[1] ,  i[2] , _id = index))
        index += 1
    
    return vertices

def populate_vertices_alt(scene) -> list:
    """
    Create a list of sprocketlib.mesh.Vertex objects
    """
    vertices = []
    index = 0
    for i in scene["vertices"]:
        print(i)
        vertices.append(spl.mesh.Vertex( -i[0] , i[1] ,  i[2] , _id = index))
        index += 1
    
    print(len(vertices))
    return vertices

def populate_faces(scene: pwf.Wavefront, thickness = 1) -> list:
    """
    Create a list of sprocketlib.mesh.Face_IDOnly objects
    """
    # TODO: Switch from Face_IDOnly to Face objects
    faces = []
    for i in scene.mesh_list[0].faces:
        faces.append(spl.mesh.Face_IDOnly(i[0], i[1], i[2], thickness=thickness))
    
    return faces

def populate_faces_alt(scene, thickness = 1) -> list:
    """
    Create a list of sprocketlib.mesh.Face_IDOnly objects
    """
    # TODO: Switch from Face_IDOnly to Face objects
    faces = []
    for i in scene["faces"]:
        try:
            faces.append(spl.mesh.Face_IDOnly(i[0], i[1], i[2], id4 = i[3], thickness=thickness))
        except IndexError:
            faces.append(spl.mesh.Face_IDOnly(i[0], i[1], i[2], thickness=thickness))
    
    return faces

def merge_duplicate_points(v: list, f: list) -> tuple:
    """
    Merge duplicate points
    """
    vertices = copy.deepcopy(v)
    faces = copy.deepcopy(f)

    ignore = []

    for vert1 in vertices:
        for vert2 in vertices:
            if vert1.coords == vert2.coords and vert2 not in ignore:
                for face in faces:
                    if face.vertex_ids[0] == vert2.id:
                        face.vertex_ids[0] = vert1.id

                    if face.vertex_ids[1] == vert2.id:
                        face.vertex_ids[1] = vert1.id

                    if face.vertex_ids[2] == vert2.id:
                        face.vertex_ids[2] = vert1.id
                    

                ignore.append(vert1)
    
    
    # TODO: Remove duplicate points. For some reason, removing points that lack any faces referencing them makes Sprocket freeze

    return (vertices, faces)
