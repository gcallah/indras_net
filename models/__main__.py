from indra.entry_point import entry_point

models = {
             "1": ("Adam Smith's Fashion Model", "fashion_run.py"),
             "2": ("Forest Fire", "forestfire_run.py"),
             "3": ("Abelian Sandpile", "sand_run.py"),
             "4": ("Wolf Sheep", "wolfsheep_run.py")
         }


def main(args=None):
    entry_point(args, models)

if __name__ == "__main__":
    main()
