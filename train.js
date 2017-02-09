const brain = require('brain.js');
const fs = require('fs');
const _ = require('underscore');

const userCnt = 50000;
const modelCnt = 20;
const favortiteModelCnt = modelCnt;

let trainingSet = [];
let net = new brain.NeuralNetwork();

  // trainingSet = body.aggregations.users.buckets.map(function(user){
  //         return {
  //           input: _.object(user.models.buckets.map(function(model){
  //             return [model.key,1];
  //           })),
  //           output: _.object(user.models.buckets.slice(0, favortiteModelCnt).map(function(model){
  //             return [model.key, model.doc_count / (user.doc_count - user.models.sum_other_doc_count)];
  //           }))
  //         };
  //       });

  trainingSet = [{input: [0, 0], output: [1]},
		           {input: [0, 1], output: [2]},
		           {input: [1, 0], output: [2]},
		           {input: [1, 1], output: [3]}
           	];
      // console.log('trainingSet', JSON.stringify(trainingSet));
      console.timeEnd('trainingSet');

      
      net.train(trainingSet,
        {
          errorThresh: 0.001,  // error threshold to reach
          iterations: 20000,   // maximum training iterations
          log: true,           // console.log() progress periodically
          logPeriod: 1,       // number of iterations between logging
          learningRate: 0.3    // learning rate
        }
      );
        
      console.timeEnd('train: userCnt = ' + userCnt);
        
      let wstream = fs.createWriteStream('./data/brain.json');
      wstream.write(JSON.stringify(net.toJSON(),null,2));
      wstream.end();



