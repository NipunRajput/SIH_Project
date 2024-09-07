const express = require('express');
const dotenv = require('dotenv');
const socialRoutes = require('./routes/socialRoutes');

dotenv.config();
const app = express();

app.use('/api/social', socialRoutes);

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
