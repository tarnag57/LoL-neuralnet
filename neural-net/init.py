import data_loader
import network

training_data, test_data = data_loader.load_data(500)

#third try
net = network.Network([1370, 1000, 2])
net.SGD(training_data, 1000, 1, 3.0, test_data = test_data)
