const brain = require('brain.js');
const fs = require('fs');
const _ = require('underscore');

const afs = require("async-file");

const userCnt = 50000;
const modelCnt = 20;
const favortiteModelCnt = modelCnt;


(async() => {
  var trainingSet = [];
  var net = new brain.NeuralNetwork();

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
    var mainDir = '../auto/';
    var dirs = await afs.readdir(mainDir)
    var autosFiles = {};

    dirs.forEach( async(item) => {
      
      ( async (d) => {
        autosFiles[d] = afs.readdir(mainDir+"audi/")
      })(item)
      

    } );

    for (var i in autosFiles){
      autosFiles[i] = await autosFiles[i];
    }

    // for (var j=0; j< 10; j++){
    //   console.log(j);
    // }

    for (var i in autosFiles){

      for (var j=0; j< autosFiles[i].length; j++){
        item = autosFiles[i][j];
        if(item.indexOf(".json") >= 0 ){
          var output = {};
              output[i] = 1;
              
              var input = JSON.parse(await afs.readFile(mainDir + i +'/'+item, 'utf8') );
              trainingSet.push({
                  input: input,
                  output: output
              });
        }
      }

      // autosFiles[i].forEach(async(item) => {



      //   // await (async function(item){
      //       if(item.indexOf(".json") >= 0 ){


      //           var output = {};
      //           output[i] = 1;
                
      //           var input = JSON.parse(await afs.readFile(mainDir + i +'/'+item, 'utf8') );
      //           // console.log(output);
      //           // var input = [1,1,1,1,1];
      //           trainingSet.push({
      //               input: input,
      //               output: output
      //           });


      //           // console.log(  JSON.parse(await afs.readFile(mainDir + i +'/'+item, 'utf8')) )  ;
      //       }

      //   // })(item)

      //   // console.log(trainingSet);
      // })

    }


    
    // dirs.forEach(async function(item){
    //   // console.log(item);

    //   autosFiles[item] = await afs.readdir(mainDir+item+"/")      

    // })


    // console.log(autosFiles);
    // console.log( await autosFiles );

    // await Promise.all(autosFiles);

    // console.log(res);
    // let data = await afs.readFile('../auto/audi/1.json')

    // console.log(dirs);

    // return;

    // trainingSet = [{input: [0, 0, 0], output: {1:1}},
  		//            {input: [0, 0,1], output: {2:1}},
  		//            {input: [0, 1,0], output: {3:1}},
  		//            {input: [0, 1, 1], output: {4:1}},
  		//            {input: [1, 0, 0], output: {5:1}},
  		//            {input: [1, 0, 1], output: {6:1}},
  		//            {input: [1, 1, 0], output: {7:1}},
  		//            {input: [1, 1, 1], output: {8:1}}
    //          	];
        // console.log('trainingSet', JSON.stringify(trainingSet));
        // console.timeEnd('trainingSet');

        
        net.train(trainingSet,
          {
            errorThresh: 0.01,  // error threshold to reach
            iterations: 5,   // maximum training iterations
            log: true,           // console.log() progress periodically
            logPeriod: 1,       // number of iterations between logging
            learningRate: 0.3    // learning rate
          }
        );
          
        console.timeEnd('train: userCnt = ' + userCnt);
          
        let wstream = fs.createWriteStream('./data/brain.json');
        wstream.write(JSON.stringify(net.toJSON(),null,2));
        wstream.end();

})();

