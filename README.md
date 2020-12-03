# A Game Theoretic Approach for Fake News Minimization 

In this modern era, social media is one of the topmost source of fake news. All social media platforms are trying to curb the spread of misinformation. This project aims towards analyzing various approaches and strategies for the fake news spreader and the platform.

# Requirements

* networkx
* numpy
* pandas
* pickle
* snap

# Installation / Setup

*Note*: If you don't have python3 then you need to install python3 on your PC.

You shall need networkx, numpy, pandas, pickle, snap for executing the code. 

You can install snap by the following the below steps.

Run this command on terminal.
```
pip3 install snap-stanford
```

Then unzip the .tar.gz file that was downloaded using the below command.

```
tar zxvf snap-stanford-5.0.0-5.0-ubuntu18.04.2-x64-py3.6.tar.gz
```

Then go to the directory.

```
cd snap-stanford-5.0.0-5.0-ubuntu18.04.2-x64-py3.6
```

Then install snap using following command.
```
sudo python3 setup.py install
```

You can install the rest of the dependencies by executing the following commands.

```
pip3 install networkx
pip3 install numpy
pip3 install pandas
pip3 install pickle
```

# Running the code

The code can be executed by the following command -

```
python3 run.py
```

The code will ask for the following inputs -

* n -> The number of nodes in the graph (Excluding oracle nodes)
* m -> The maximum number of outgoing edges from a node (where minimum number of outgoing edge from each node is 1)
* num_bots -> The number of oracle nodes in the graph
* edges_per_bot -> The number of nodes in graph being monitored by each oracle node
* size_activators -> The approximate number of outgoing edges from activator nodes (actual value is >= size_activators)
* exponent_activators -> Value of Activator exponent used by the misinformation spreader to choose the activator set
* exponent_bots -> Value of oracle exponent used by the platform to choose the nodes to be directly connected by the oracle nodes
* num_iters -> Number of iterations of spread of the misinformation from the sources, i.e. the activator and misinformed nodes 

## Contributors
* [Aditya Singh Chauhan](https://github.com/adityasc)
* [Akhilesh Sharma](https://github.com/Dragnoid99)
* [Mohd Talib Siddiqui](https://github.com/the-mts)
* [Sanchit Agrawal](https://github.com/Roberticey)
* [Shashwat Gupta](https://github.com/shashwat2110)
