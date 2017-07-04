from indra.entry_point import entry_point

models = {
    "1": ("Segregation", "segregation_run.py"),
    "2": ("Height", "height_run.py"),
    "3": ("Auditorium", "auditorium_run.py")
     }


def main(args=None):
    entry_point(args, models)

if __name__ == "__main__":
    main()
