const axios = require('axios');

const getFacebookData = async (req, res) => {
    const token = process.env.FACEBOOK_ACCESS_TOKEN;
    const url = `https://graph.facebook.com/v12.0/me?fields=id,name,posts{message,created_time}&access_token=${token}`;

    try {
        const response = await axios.get(url);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching Facebook data' });
    }
};

module.exports = { getFacebookData };
