"""
Indra's Net is an agent-based modeling framework for creating ABMs in Python.
The framework provides the ABM developer with:
    *    Looping over agents randomly, in order, in reverse order, or by type. 
    *    Automatic generation of line graphs and scatter plots. 
    *    The ability to enter model parameters interactively, from the command
    line, or from a file. 
    *    The ability to save parameters sets. 
    *    The ability to dump the state of the system to a JSON file. 
    *    The ability to save results to a CSV file for processing by R, Excel,
    etc.
    *    A built-in, extensible interactive menu. 
    *    Automatic creation of network graphs showing the relationship among
    objects in the system. 
    *    Extensible Markov-matrix capabilities for easily specified,
    probabilistic behavior on the part of agents. 
    *    A flexible spatial environment model that allows the composition of
    agent views of the environment of any desired shape, easing the creation of
    models exploring limited, local agent knowledge. 
    *    In-line debugging capabilities, allowing, e.g., display of an agent's
    attributes at any point during the run of a model. 
    *    The ability to step through a model to watch it develop in real time. 
Models in Indra make use of the library facilities contained in the indra
module. Generally speaking, one subclasses an existing model (such as a grid
model), develops one's own code, and then runs the model with a run file.
Model files are named x_model.py, and run files x_run.py.

To get going with Indra, it is recommended that one begin by copying a simple
model, such as basic_model.py or grid_model.py, and copying the accompanying
run file (basic_run.py or grid_run.py), and start modifying these files to
understand how they work.
If one has a model similar to one already built, copying that model's
x_model.py file and x_run.py file might be a better bet.

Although matplotlib and clint packages are not required, you can gain
additional capabilities by installing them.
"""
