from pybrain.tools.shortcuts import buildNetwork

from pybrain.structure import TanhLayer
from pybrain.structure import SoftmaxLayer

from pybrain.datasets import SupervisedDataSet

from pybrain.supervised.trainers import BackpropTrainer




net = buildNetwork(2, 3, 1, hiddenclass=TanhLayer, bias=True)
ds = SupervisedDataSet(2, 1);

ds.addSample((0, 0), (0,))
ds.addSample((0, 1), (1,))
ds.addSample((1, 0), (1,))
ds.addSample((1, 1), (0,))


trainer = BackpropTrainer(net, ds)

trainer.train()




#net.activate([2, 1])