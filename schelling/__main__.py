from indra.entry_point import entry_point
import schelling.height_run
import schelling.auditorium_run
import schelling.segregation_run

models = {
    1: ("Segregation", schelling.segregation_run.run),
    2: ("Height", schelling.height_run.run),
    3: ("Auditorium", schelling.auditorium_run.run)
     }


def main(args=None):
    entry_point(args, models)

if __name__ == "__main__":
    main()
