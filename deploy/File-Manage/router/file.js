const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');
const multer = require('multer');

const storage = multer.diskStorage({
	destination: (req, file, cb) => {
		cb(null,path.join(__dirname,"../public/"));
	},
	filename: (req, file, cb) => {
		const fileName = req.body.fileName;
		const fileType = req.body.fileType;
		if (!fileName || !fileType) {
      return cb(new Error('Missing fileName or fileType in request body'));
    }
		cb(null,fileName + '.' + fileType);
	}
})

const upload = multer({ storage: storage });

router.post('/file',upload.single('file'),(req,res)=>{
	res.json({message:"success"})
})

router.get('/file',(req,res)=>{
	const fileName = req.query.fileName;

	if (!fileName){
		res.status(400).json({err:"missing filename value"});
	}
	if (typeof fileName !== 'string'){
		res.status(400).json({err:"filename type should be string"});
	}

	let file = path.join(__dirname,"../public/",fileName);
	console.log(file);

	fs.access(file,fs.constants.F_OK, (err) => {
		if(err){
			console.log(err.message)
			return res.status(404).json({err:"no such file"});
		}
		res.sendFile(file);
	})

});

router.delete('/file',(req,res)=>{
	const fileName = req.query.fileName;
	if (!fileName){
		res.status(400).json({err:"missing filename value"});
	}

	const filePath = path.join(__dirname, '../public/', fileName);
  fs.unlink(filePath, (err) => {
    if (err) {
			console.log(err.message)
      return res.status(500).json({ err: 'Failed to delete file'});
    }
    res.json({ message: 'File deleted successfully' });
  });
})

module.exports=router; 