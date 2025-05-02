require("dotenv").config();
const express=require('express');
const helmet=require('helmet');
const logger=require('./utils/logger');
const cors=require('cors');
const serviceRoutes=require("./route/route.js")
const bodyParser=require('body-parser')
const PORT=process.env.PORT||3000;

const app=express();

app.use(express.json())
app.use(cors({
    origin:true,
    credentials:true
}))
app.use(bodyParser.json());

app.use(helmet()); //prevent from xss and other vulnerabilities

app.use('/api',serviceRoutes);




app.listen(PORT,()=>{
    console.log('visualization service running on port ',PORT);
  })