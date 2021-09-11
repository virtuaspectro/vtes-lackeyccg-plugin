const unzip = require('unzip-stream');
const fs = require('fs');

const basePath = (path) => `${process.cwd()}/${path}`;

const oldPath = basePath('vtescsv/old');
const newPath = basePath('vtescsv/new');

const extract = (done, failed) => {
  fs.createReadStream(basePath('vtescsv/vtescsv_utf8.zip')).pipe(
    unzip
      .Extract({ path: newPath })
      .on('close', () => {
        console.log('CSV Files Extracted');
        done();
      })
      .on('error', () => failed(new Error('Unzip Failed'))),
  );
};

const move = (done, failed) => {
  fs.readdir(newPath, (err, files) => {
    if (err) {
      failed(err);
      return;
    }
    files.forEach((file) => {
      const from = `${newPath}/${file}`;
      const to = `${oldPath}/${file}`;

      fs.rename(from, to, function (err) {
        if (err) {
          if (err.code === 'EXDEV') {
            copy(done, failed);
          } else {
            failed(err);
          }
          return;
        }
        done();
        console.log('CSV files updated');
      });
    });
  });
};

const copy = (done, failed) => {
  var readStream = fs.createReadStream(newPath);
  var writeStream = fs.createWriteStream(oldPath);

  readStream.on('error', failed);
  writeStream.on('error', failed);

  readStream.on('close', function () {
    fs.unlink(newPath, done);
    console.log('CSV files updated with copy method');
  });

  readStream.pipe(writeStream);
};

const getCSVFiles = async () => {
  await new Promise(extract);
  await new Promise(move);
};

module.exports = { basePath, getCSVFiles };
