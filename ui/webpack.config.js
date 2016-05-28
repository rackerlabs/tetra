var webpack = require('webpack');

module.exports = {
    // babel will run and put all the files in .dist
    entry: './dist/main.js',
    output: {
        path: './dist',
        filename: 'tetra.bundle.js',
    },

    // disable warnings from third-party code
    plugins: [
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            }
        })
    ],
}
