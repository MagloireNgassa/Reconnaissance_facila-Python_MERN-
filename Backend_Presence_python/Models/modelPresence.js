const mongoose = require('mongoose');  

const presenceSchema =  mongoose.Schema({
    nom:String,
    date:String,
    time:String,
    photo:String
    
});

module.exports = mongoose.model('presence', presenceSchema);

