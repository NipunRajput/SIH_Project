const axios = require('axios');

const getInstagramData = async (req, res) => {
    const token = process.env.INSTAGRAM_ACCESS_TOKEN;
    const url = `https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,thumbnail_url,timestamp&access_token=${token}`;

    try {
        const response = await axios.get(url);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching Instagram data' });
    }
};

module.exports = { getInstagramData };
