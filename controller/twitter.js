const axios = require('axios');
const qs = require('qs');

const getTwitterData = async (req, res) => {
    const twitterKey = process.env.TWITTER_API_KEY;
    const twitterSecret = process.env.TWITTER_API_SECRET;
    const token = Buffer.from(`${twitterKey}:${twitterSecret}`).toString('base64');

    try {
        // Get bearer token
        const response = await axios.post('https://api.twitter.com/oauth2/token', qs.stringify({ grant_type: 'client_credentials' }), {
            headers: {
                Authorization: `Basic ${token}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        const bearerToken = response.data.access_token;

        // Use the bearer token to make API requests
        const tweets = await axios.get('https://api.twitter.com/1.1/statuses/user_timeline.json?count=10', {
            headers: { Authorization: `Bearer ${bearerToken}` }
        });

        res.json(tweets.data);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching Twitter data' });
    }
};

module.exports = { getTwitterData };
