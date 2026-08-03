module.exports = {
  dbType: 'postgres',
  apiSecret: process.env.CUBEJS_API_SECRET || 'cube_secret',
  devServer: true,
};
