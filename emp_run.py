import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, filemode='w', filename="log.txt")

logging.info("Starting program")

ronnie = EconAgent("manager", 10000.00, "Ronnie")
suzanne = EconAgent("manager", 20000.0, "Suzanne")
sandy = EconAgent("manager", 10000.00, "Sandy")
connie = EconAgent("manager", 10000.00, "Connie")
rich = EconAgent("manager", 10000.00, "Rich")
gene = EconAgent("worker", 10.00, "Gene")
shruti = EconAgent("worker", 10.00, "Shruti")
cedric = EconAgent("worker", 10.00, "Cedric")
sandy.add_employee(gene)
sandy.add_employee(shruti)
sandy.add_employee(cedric)
ronnie.add_employee(connie)
ronnie.add_employee(sandy)
suzanne.add_employee(ronnie)
suzanne.add_employee(rich)

suzanne.walk_graph_breadth_first(print_econ_agent, True)

