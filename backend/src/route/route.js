const {handleCodeValidation, handleGenerateTrace}=require("../controllers/controller")
const express=require('express')
const router=express.Router()

router.post('/validate',handleCodeValidation);

router.post('/trace',handleGenerateTrace)
module.exports=router