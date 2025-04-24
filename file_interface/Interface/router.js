const express = require('express');
const router = express.Router();

const file = require('./router/file');
router.use('/',file);

module.exports=router;