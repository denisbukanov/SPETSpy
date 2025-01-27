import blueprint.bphandler as bphandler
import blueprint.filehandler as filehandler
import blueprint.out as out

import mesh.objhandler as objhandler

from logger import logger
from typing import Annotated
from pathlib import Path
import typer
import json
import os

app = typer.Typer()


def load_model(objpath: str) -> tuple[list, list]:
    scene = objhandler.create_scene(objpath)
    vertices = objhandler.populate_vertices(scene)
    faces = objhandler.populate_faces(scene)
    #  scene = objhandler.load_shape_from_obj(objpath, raw=False)
    #  vertices = objhandler.populate_vertices_alt(scene)
    #  faces = objhandler.populate_faces_alt(scene)

    vertices, faces = objhandler.merge_duplicate_points(vertices, faces)
    vertices = out.reformat_vertices(vertices)
    faces = out.reformat_faces(faces)
    reveal_type(vertices)
    reveal_type(faces)
    return vertices, faces


def objpath_callback(objpath: Path) -> Path:
    if not objpath.exists() or not objpath.is_file():
        err = 5
        logger.error("File not found: %s, Aborting with error code %d.", objpath, err)
        raise typer.Exit(code=err)
    return objpath


@app.command()
def importer(objpath: Annotated[Path, typer.Argument(callback=objpath_callback)], compartment: str, asVehicle: str = ""):
    """
    Import .obj file as sprocket compartment or into vehicle if --asVehicle is specified

    if --asVehicle is specified, then put faction and vehicle in the format "Faction.Vehicle", including quotes
    """

    faces, vertices = load_model(str(objpath))
    # TODO: implement compartment-only generation
    if asVehicle != "":
        factionsFolder = filehandler.get_factions_folder()
        # TODO: Implement proper fix
        if not os.path.exists(factionsFolder):
            err = 4
            logger.error("Faction folder not found at %s. Please enter path below.", factionsFolder)
            factionsFolder = typer.prompt("Folder containing Factions")
        factions = filehandler.get_factions(factionsFolder)

        faction, vehicle = asVehicle.split(".")

        if faction not in factions:
            err = 1
            logger.error("Faction not found, please choose from %s. Aborting with error code %d.", factions, err)
            raise typer.Exit(code=err)

        vehiclesFolder = filehandler.get_vehicles_folder(factionsFolder, faction)
        vehicles = filehandler.get_vehicles(vehiclesFolder)

        if vehicle not in vehicles:
            err = 2
            logger.error("Vehicle not found, please choose from %s. Aborting with error code %d.", vehicles, err)
            raise typer.Exit(code=err)
        vData = filehandler.load_bp_as_dict(filehandler.get_vehicle_path(vehiclesFolder, vehicle))
        vuid = bphandler.get_vuid(vData, compartment)
        if vuid is None:
            err = 3
            logger.error("Compartment %s not found. Aborting with error code %d.", compartment, err)
            raise typer.Exit(code=err)

        template = out.fill_template(vuid, vertices, faces)[0]

        cData = {
            'meshes': [template]
        }

        found = False
        for mesh in vData['meshes']:
            if mesh['vuid'] == vuid:
                mesh['meshData']['mesh'] = cData['meshes'][0]['meshData']['mesh']
                found = True

        if not found:
            err = 3
            logger.error("Compartment %s not found. Aborting with error code %d.", compartment, err)
            raise typer.Exit(code=err)

        with open(filehandler.get_vehicle_path(vehiclesFolder, vehicle), 'w') as vFile:
            json.dump(vData, vFile, indent='  ')

        return ("Completed", 0)
    else:
        print("Nothing to do, exiting.")


if __name__ == "__main__":
    app()
