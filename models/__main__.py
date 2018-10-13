from indra.entry_point import entry_point
import models.fashion_run
import models.forestfire_run
import models.sand_run
import models.wolfsheep_run

models = {
             1: ("Adam Smith's Fashion Model", models.fashion_run.run),
             2: ("Forest Fire", models.forestfire_run.run),
             3: ("Abelian Sandpile", models.sand_run.run),
             4: ("Wolf Sheep", models.wolfsheep_run.run)
         }


def main(args=None):
    entry_point(args, models)

if __name__ == "__main__":
    main()
