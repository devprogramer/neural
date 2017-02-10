const brain = require('brain.js'),
      fs = require('fs'),
      mnist = require('mnist'),
      softmax = require('./lib/softmax');



(async() => {

	// fs.readFile('./data/brain.json', 'utf8', function(err, contents) {
	//     console.log(contents);
	// });

	// fs.read(fd, buffer, offset, length, position, callback)

	var net = new brain.NeuralNetwork();
	const set = mnist.set(1, 0, 1);
	//const trainingSet = set.training;
	const testSet = set.test;
	net.fromJSON(require('./data/brain'));
	var output = net.run([1,0,1]);
	var maxRes = 0;
	var res = null;
	for (var i in output){
		if(output[i]> maxRes){
			maxRes = output[i]; 
			res = i;
		}
	}
	console.log(testSet[0].output);
	console.log(maxRes, res);    
})();




// console.log(softmax(output));

