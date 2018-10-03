const makeConfig = require('sc-recipe-staticresources');


module.exports = makeConfig(
  // name
  'brasil.gov.agenda',

  // shortName
  'brasilgovagenda',

  // path
  `${__dirname}/../src/brasil/gov/agenda/browser/static`,

  //publicPath
  '++resource++brasil.gov.agenda/',

  //callback
  function(config, options) {
    config.entry.unshift(
      './app/img/agenda_icon.png',
      './app/img/compromisso_icon.png',
    );
  },
);
