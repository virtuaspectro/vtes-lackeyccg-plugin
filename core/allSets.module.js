const csv = require('csvtojson');
const fs = require('fs');
const { basePath } = require('./file.module');

module.exports = {
  CSV_FILES: ['vtescrypt.csv', 'vteslib.csv'],
  csvPath: function (fileName) {
    return basePath(`vtescsv/new/${fileName}`);
  },
  allSetsPath: function () {
    return basePath(`vtes-plugin/high/allsets.txt`);
  },
  parser: function (json) {
    const samples = [];
    json.forEach((card) => {
      try {
        const text = card['Card Text'];
        const expansions = this.parseCardSet(card.Set, card.Type);
        const cardText = text ? text.replace(/(?:\r\n|\r|\n)/g, ' ') : '';

        const cardData = [
          `${this.removeSpecialChars(card.Name)}${card.Adv ? ' (ADV)' : ''}`,
          expansions.firstSet,
          this.getImageFileName(card.Name, card.Adv, card.Type),
          expansions.lastSet.split('-')[0],
          card.Type,
          card.Clan,
          card.Group,
          card.Capacity,
          card.Disciplines || card.Discipline,
          card.PoolCost,
          card.BloodCost,
          this.removeSpecialChars(cardText),
          card.Set.replace(/Promo-\d+/, 'Promo'),
          this.removeSpecialChars(card.Artist),
        ];

        samples.push(cardData.join('\t'));
      } catch (e) {
        console.error(e);
      }
    });
    return samples.join('\n');
  },
  parseCardSet: function (set, type) {
    const setList = set.split(',');
    const setSize = setList.length;
    let lastSet = setList[setSize - 1].split(':')[0];
    let firstSet = setList[0].split(':')[0].split('-')[0];

    if (this.isCrypt(type)) firstSet += 'M';

    return { firstSet, lastSet };
  },
  isCrypt: function (type) {
    return ['Imbued', 'Vampire'].some((t) => t === type);
  },
  getImageFileName: function (name, adv, type) {
    const fullName = name + (adv ? 'adv' : '');
    let imageName = this.simplifyName(fullName);

    if (this.isCrypt(type)) imageName += ',cardbackcrypt';

    return imageName;
  },
  removeSpecialChars: function (name) {
    return name
      .normalize('NFD') // Converte os caracteres acentuados em caracteres regulares
      .replace(/[\u0300-\u036f|\{|\}|\/]/g, '')
      .replace(/[\-|\—|\-]/g, '-')
      .replace(/\œ/, 'oe')
      .replace('  ', ' ');
  },
  simplifyName: function (name) {
    if (!name) return '';

    return name
      .normalize('NFD') // Converte os caracteres acentuados em caracteres regulares
      .replace(/[\u0300-\u036f|\s|,|\.|\"|\'|\-|\!|\:|\(|\)|\—|\/]/g, '') // Range do Unicode para aplicar a conversão, e mais outros caracteres
      .replace(/\œ/, 'oe') // Para lidar com nomes como 'Sacré-Cœeur Cathedral, France'
      .toLowerCase(); // Converte tudo para Lower Case
  },
  generate: async function () {
    let outputLackey = `Name\tSET\tImageFile\tExpansion\tType\tClan\tGroup\tCapacity\tDiscipline\tPoolCost\tBloodCost\tText\tRarity\tArtist\n`;

    for (let filename in this.CSV_FILES) {
      const file = fs.readFileSync(this.csvPath(this.CSV_FILES[filename]), {
        encoding: 'utf8',
      });
      const csvRow = await csv().fromString(file);
      outputLackey += this.parser(csvRow);
      outputLackey += '\n';
    }

    fs.writeFileSync(this.allSetsPath(), `${outputLackey}\n`);
    console.log(`ALL SETS file created on ${this.allSetsPath()}`);
  },
  integrityCheck: function (cardLists) {
    const allSetsFile = fs.readFileSync(this.allSetsPath(), {
      encoding: 'utf8',
    });
    const lines = allSetsFile.split('\n');
    const names = lines.map((line) => this.simplifyName(line.split('\t')[0]));

    const notFound = [];

    ['crypt', 'library'].forEach((type) => {
      cardLists[type].new.every((card) => {
        const check = names.includes(
          this.simplifyName(card.Name + (card.Adv ? 'adv' : '')),
        );
        if (check) {
          return true;
        }
        notFound.push(card.Name);
      });
    });
    console.log(notFound);
  },
};
