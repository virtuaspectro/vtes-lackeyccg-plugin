const csv = require('csvtojson');
const fs = require('fs');
const { basePath } = require('./file.module.js');

const libraryOld = basePath(`/vtescsv/old/vteslib.csv`);
const cryptOld = basePath(`/vtescsv/old/vtescrypt.csv`);
const libraryNew = basePath(`/vtescsv/new/vteslib.csv`);
const cryptNew = basePath(`/vtescsv/new/vtescrypt.csv`);

const getJsonFromCSV = (path) => {
  const file = fs.readFileSync(path, { encoding: 'utf8' });
  return csv().fromString(file);
};

const getCardLists = async () => {
  const cardLists = {
    library: {
      old: null,
      new: null,
    },
    crypt: {
      old: null,
      new: null,
    },
  };

  const results = await Promise.all([
    getJsonFromCSV(libraryOld),
    getJsonFromCSV(libraryNew),
    getJsonFromCSV(cryptOld),
    getJsonFromCSV(cryptNew),
  ]);

  cardLists.library.old = results[0];
  cardLists.library.new = results[1];
  cardLists.crypt.old = results[2];
  cardLists.crypt.new = results[3];

  return cardLists;
};

module.exports = { getCardLists, getJsonFromCSV };
