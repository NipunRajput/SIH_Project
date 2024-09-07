const express = require('express');
const { getFacebookData } = require('../controller/facebook');
const { getTwitterData } = require('../controller/twitter');
const { getInstagramData } = require('../controller/instagram');

const router = express.Router();

router.get('/facebook', getFacebookData);
router.get('/twitter', getTwitterData);
router.get('/instagram', getInstagramData);

module.exports = router;
