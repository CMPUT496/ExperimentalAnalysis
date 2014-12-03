#CMPUT 496 Project Readme
Authored by: Tyler Wendlandt & Matthew Fritze

##Important Files
`Simulator/sim.py` - implemented by Matthew & Tyler

`sim.py` contains all the code for the actual simulator portion of the project. It has the model for the line configurations, as well as the student configurations (which inherits from lineConfig). The `distance` function computes the distance between a line configuration and a student configuration, `probability` returns the probabiltity of succes for a student trying a problem, and `simulate` is the function which is called by algorithms to run a simulation of a student against a passed number line configuration.

`main.py`


###Algorithms
`egreedy.py` - implemented by Tyler

This contains our implementation of egreedy with a arm pull budget. `egreedy(students, arms, bound, epsilon, log_file)` takes 5 arguments:
* `students` is a list of student objects retrieved from the simulator in the `main.py`
* `arms` is a list of number line configurations which is retrieved from one of our config files found in the directory `Simulator/configs`.
* `bound` is the budget of arm pulls for the algorithm
* `epsilon` is the desired epsilon parameter for egreedy as per usual
* `log_file` is a `FILE` object where all logs will be written to. 

`sequential_halving.py` - implemented by Tyler

This contains our implementation of sequential halving. `sequential_halving(students, arms, bound, log_file)` takes 4 arguments:
* `students` is a list of student objects retrieved from the simulator in the `main.py`
* `arms` is a list of number line configurations which is retrieved from one of our config files found in the directory `Simulator/configs`
* `bound` is the budget of arm pulls for the algorithm
* `log_file` is a `FILE` object where all logs will be written to. 

`lil_ucb.py` - implemented by Matthew

This contains our implementation of lil'UCB. `lil_ucb(students, arms, delta, epsilon, lambda_p, beta, sigma, log_file, max_pulls)` takes 9 arguments:
* `students` is a list of student objects retrieved from the simulator in the `main.py`
* `arms` is a list of number line configurations which is retrieved from one of our config files found in the directory `Simulator/configs`.
* `delta` Parameters spefified on page 10 of lil'UCB paper as lil'UCB (+LS)
* `epsilon` ''
* `lamdba_p` ''
* `beta` ''
* `sigma` ''
* `log_file` is a `FILE` object where all logs will be written to. 
* `max_pulls` is the budget of arm pulls for the algorithm


##How to run
###general command
to run our experiments we run the following command from the `Simulator/` directory:

```
# $alg = algorithm choice {0, 1, 2}
# $logfile = name of file you'd like to log your results to
# $configfile = name of config file you woul like to read from
python main.py $alg $logfile $configfile [optional extra arguments]
```


###Running with epsilon-greedy
To run an experiment with epsilon-greedy we need `$alg = 0`, for our experiments we ran egreedy with the following extra parameters: `0.1 100000`, which uses epsilon = 0.1 and arm pull budget of 100000 pulls.

Example run: `python main.py 0 logfile.log configs_base.in 0.1 100000`

###Running with lil'UCB
To run an experiment with lil'UCB we need `$alg = 1`, and it takes no extra parameters.

Example run: `python main.py 1 logfile.log config_base.in`

###Running with sequential halving
To run an experiment with sequential halving we need `$alg = 2`, for our experiments we ran egreedy with the following extra parameters: `100000`, which uses an arm pull budget of 100000 pulls.

Example run: `python main.py 2 logfile.log configs_base.in 100000`

###How to use extra parameters (experiment)
To use our extra parameters you simply have to use the appropriate `configfile`. The default config file for our base experiments is `configs_base.in`. For extra params 1, we use `configs_1.in`, and for extra params 2 we use `configs_2.in`.

##How to change distribution
we had used a very hackish way of altering distributions. To set the simulator to small distribution open the `Simulator/sim.py` file and uncomment all the lines that have the `# add this line for small dist` comment

To get large dist uncomment all the lines that have the line `# add this line for large dist` comment. In the student model under the constructor switch the following line...
```
from...
self.s_lambda = numpy.random.normal(1, .1) 
to...
self.s_lambda = numpy.random.normal(1, 5)
```
odd I know, but it got us fairly different distributions.
