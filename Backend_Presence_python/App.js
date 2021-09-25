const express = require('express');
const cors = require('cors');  
const app = express();
app.use(cors());

const mongoose = require('mongoose');
const connection = mongoose.connection;

var bodyParser = require('body-parser'); 
const Presence = require('./Models/modelPresence');
app.use(bodyParser.json());                            
app.use(bodyParser.urlencoded({ extended: true })); 

//mongoose.connect('mongodb://localhost:27017/PresenceBd',{ useUnifiedTopology: true, useNewUrlParser: true });

mongoose.connect('mongodb+srv://SaoGroupe:barnou052018@clustersaogroupe.n7o0s.mongodb.net/PresenceDB?retryWrites=true&w=majority');

//mongoose.connect('mongodb://mngassa:mngassa@10.30.40.121:27017/mngassa',{​​​​​​​ useUnifiedTopology: true, useNewUrlParser: true }​​​​​​​  );

/*const PORT = 3019;
app.listen(PORT,()=>{                                  
    console.log("j'écoute le port 3019!!");
});*/
const PORT = 3535;
app.listen(PORT,()=>{                                  
    console.log("j'écoute le port 3535!!");
});                                                     

connection.once('open',()=>{
    console.log("connected to MongoDb");
});

 app.post('/presence',(req, res)=>{                  
    console.log('req.body', req.body);             
    const presenceAdd = new Presence(req.body);        
    presenceAdd.save((err, presenceAdd)=>{                 
        if(err){
            return res.status(500).json(err);           
        }
        res.status(201).json(presenceAdd);                
    });
}); 

app.get('/presenceAll',(req,res)=>{
    Presence.find()
    .exec()
    .then(presence => res.status(200).json(presence));
});

app.get('/presenceDate/:phone',(req,res)=>{
    const phone = req.params.phone;
    Client.find({date:phone})
    .exec()
    .then(client => res.status(200).json(client));
});

 
 