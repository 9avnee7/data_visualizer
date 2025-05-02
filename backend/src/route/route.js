const {handleCodeValidation,uploadCodeToS3, handleGenerateTrace}=require("../controllers/controller")
const express=require('express')
const router=express.Router()

router.post('/validate',handleCodeValidation);
// router.post('/uploadtos3',uploadCodeToS3);
router.post('/trace',handleGenerateTrace)
module.exports=router