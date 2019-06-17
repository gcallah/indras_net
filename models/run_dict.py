from basic import main as bamain
from basic import set_up as baset_up
from fashion import main as famain
from fashion import set_up as faset_up
from forestfire import main as ffmain
from forestfire import set_up as ffset_up
from sandpile import main as spmain
from sandpile import set_up as spset_up
from segregation import main as semain
from segregation import set_up as seset_up
from wolfsheep import main as wsmain
from wolfsheep import set_up as wsset_up


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
