var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var combineLoaders = require('webpack-combine-loaders');
var path = require('path');

var BUILD_DIR = path.resolve(__dirname, 'frontend/src/elec_finals/');
var APP_DIR = __dirname;

var config = {
    entry: {
        build1: `${APP_DIR}/frontend/Window1/main.jsx`,
        build2: `${APP_DIR}/frontend/Window2/secondary.jsx`,
        build3: `${APP_DIR}/frontend/Window3/buddy.jsx`,
    },
    output: {
        path: BUILD_DIR,
        filename: '.[name].js',
    },
    plugins: [
        new ExtractTextPlugin(`${BUILD_DIR}.styles.css`),
    ],
    module: {
        loaders: [{
            test: /\.jsx?$/,
            include: APP_DIR,
            loader: 'babel-loader',
            exclude: /node_modules/,
            query: {
                presets: ['react'],
            },
        }, {
            test: /\.css$/,
            loader: combineLoaders([{
                loader: 'style-loader',
            }, {
                loader: 'css-loader',
                query: {
                    modules: true,
                    localIdentName: '[name]__[local]___[hash:base64:5]',
                },
            }]),
        },
        { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader?limit=10000&mimetype=application/font-woff" },
        { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader" },
        {
          test: /\.(png|jpe?g|gif|svg|woff|woff2|ttf|eot|ico)$/,
          loader: 'file-loader?name=assets/[name].[hash].[ext]'
        }
    ],
    },
};

module.exports = config;
