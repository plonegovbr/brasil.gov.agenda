const ExtractTextPlugin = require('extract-text-webpack-plugin');
const SpritesmithPlugin = require('webpack-spritesmith');

module.exports = {
  entry: [
    './app/img/agenda_icon.png',
    './app/img/compromisso_icon.png',
    './app/brasilgovagenda.scss',
    './app/brasilgovagenda.js',
  ],
  output: {
    filename: 'brasilgovagenda.js',
    library: 'brasilgovagenda',
    libraryTarget: 'umd',
    path: `${__dirname}/../src/brasil/gov/agenda/static`,
    publicPath: '++resource++brasil.gov.agenda/',
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /(\/node_modules\/|test\.js$|\.spec\.js$)/,
      use: 'babel-loader',
    }, {
      test: /\.scss$/,
      use: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: [
          'css-loader',
          'postcss-loader',
          'sass-loader'
        ]
      }),
    }, {
      test: /.*\.(gif|png|jpe?g|svg)$/i,
      use: [
        {
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            context: 'app/',
          }
        },
        {
          loader: 'image-webpack-loader',
          query: {
            mozjpeg: {
              progressive: true,
            },
            pngquant: {
              quality: '65-90',
              speed: 4,
            },
            gifsicle: {
              interlaced: false,
            },
            optipng: {
              optimizationLevel: 7,
            }
          }
        }
      ]
    }]
  },
  plugins: [
    new ExtractTextPlugin({
      filename: 'brasilgovagenda.css',
      allChunks: true
    }),
    new SpritesmithPlugin({
      src: {
        cwd: 'app/sprite',
        glob: '*.png'
      },
      target: {
        image: 'app/img/sprite.png',
        css: 'app/scss/_sprite.scss'
      },
      apiOptions: {
        cssImageRef: './img/sprite.png'
      }
    }),
  ]
}
