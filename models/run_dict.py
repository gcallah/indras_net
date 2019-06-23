from models.basic import main as bamain
from models.basic import set_up as baset_up
from models.fashion import main as famain
from models.fashion import set_up as faset_up
from models.forestfire import main as ffmain
from models.forestfire import set_up as ffset_up
from models.sandpile import main as spmain
from models.sandpile import set_up as spset_up
from models.segregation import main as semain
from models.segregation import set_up as seset_up
from models.wolfsheep import main as wsmain
from models.wolfsheep import set_up as wsset_up


rdict = {
    "basic": bamain,
    "fashion": famain,
    "forestfire": ffmain,
    "sandpile": spmain,
    "segregation": semain,
    "wolfsheep": wsmain,
}

setup_dict = {
    "basic": baset_up,
    "fashion": faset_up,
    "forestfire": ffset_up,
    "sandpile": spset_up,
    "segregation": seset_up,
    "wolfsheep": wsset_up,
}
