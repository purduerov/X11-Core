const fs = require('fs');
const srcdir = process.argv[2];
const outdir = process.argv[3];
const packets = require(srcdir + 'packets.js');

const pak = {
    "dearflask": packets.dearflask,
    "dearclient":packets.dearclient
  };
 const jsonObj = JSON.stringify(pak);
   
 fs.writeFile(outdir + "packets.json", jsonObj, 'utf8', function (err) {
    if (err) {
        console.log("An error occured while writing JSON Object to File.");
            return console.log(err);
        }
                              
    console.log("JSON file has been saved.");
});
