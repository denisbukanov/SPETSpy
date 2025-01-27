import json
import os

import sprocketlib as spl

FACTIONS_DIR = os.path.join("OneDrive", "Documents", "My Games", "Sprocket", "Factions")


def load_bp(filepath: str):
    """
    Convert .blueprint file into sprocketlib.base.BluePrint object
    """
    bp = spl.base.BluePrint(filepath)
    return bp

def load_bp_as_dict(filepath: str) -> dict:
    """
    Convert .blueprint to python dictionary
    """
    with open(filepath, 'r') as src:
        return json.load(src)

def get_factions_folder() -> str:
    """
    Return path to folder containing factions
    """
    user_dir = os.environ.get("USERPROFILE", "")
    return os.path.join(user_dir, FACTIONS_DIR)

def get_factions(factions_folder: str) -> list[str]:
    """
    Return list of factions
    """
    return [entry.name for entry in os.scandir(factions_folder) if entry.is_dir()]

def get_vehicles_folder(factions_folder, faction) -> str:
    """
    Return path to folder containing vehicles of a given faction
    """
    return os.path.join(factions_folder, faction, 'Blueprints', 'Vehicles')

def get_vehicles(vehicles_folder: str) -> list[str]:
    """
    Return list of vehicles in a faction
    """
    vehicles = [
        os.path.splitext(entry.name)[0]
        for entry in os.scandir(vehicles_folder)
        if entry.is_file() and os.path.splitext(entry.name)[1] == '.blueprint'
    ]
    return vehicles

def get_vehicle_path(vehicles_folder: str, vehicle_name: str) -> str:
    """
    Return path to the vehicle blueprint with a given name
    """
    return os.path.join(vehicles_folder, f'{vehicle_name}.blueprint')
