const https = require('https');
const fs = require('fs');
const { basePath } = require('./file.module');

let done;
let failed;

const prepareDownloadIfNeeded = (url, method) => {
  if (method === 'HEAD') return;
  const segments = url.split('/');
  const filePath = basePath(`/vtescsv/${segments[segments.length - 1]}`);
  fs.unlink(filePath, () => {});
  const file = fs.createWriteStream(filePath);
  return file;
};

const makeRequest = (url, method, body) => {
  const file = prepareDownloadIfNeeded(url, method);
  let total = 0;
  const request = https.request(url, { method, body }, (res) => {
    switch (method) {
      case 'HEAD':
        done(res.headers);
        break;
      case 'GET':
      case 'POST':
        const contentLength = res.headers[`content-length`];

        res.on('data', (data) => {
          total += data.length;
          const percent = parseInt((total / contentLength) * 100);
          let message = `[${String(percent)}%] Downloading ${url}`;

          if (percent === 100) message = `Downloaded ${url}\n`;

          process.stdout.clearLine();
          process.stdout.cursorTo(0);

          file.write(data);

          process.stdout.write(message);
        });
        break;

      default:
        failed(new Error('[makeRequest] HTTP Method not present'));
    }
  });

  if (method !== 'HEAD') {
    request.on('close', () => {
      done(true);
    });
  }

  request.end();
  request.on('error', failed);
};

const createRequest = (url, method = 'HEAD', body = null) => {
  return new Promise((resolve, reject) => {
    done = resolve;
    failed = reject;
    makeRequest(url, method, body);
  });
};

const getHeader = (url) => {
  return createRequest(url, 'HEAD');
};

const download = (url) => {
  return createRequest(url, 'GET');
};

module.exports = {
  getHeader,
  download,
};
