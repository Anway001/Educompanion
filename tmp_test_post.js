const fs = require('fs');
const http = require('http');

function post(port){
  return new Promise((resolve) => {
    const filepath = 'educompanion-ui/public/logo192.png';
    const boundary = '----WebKitFormBoundary' + Math.random().toString(16).slice(2);
    const stats = fs.statSync(filepath);
    const filename = filepath.split('/').pop();

    const pre = Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${filename}"\r\nContent-Type: image/png\r\n\r\n`);
    const post = Buffer.from(`\r\n--${boundary}--\r\n`);

    const options = {
      hostname: '127.0.0.1',
      port: port,
      path: '/api/visuals/generate',
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data; boundary=' + boundary,
        'Content-Length': pre.length + stats.size + post.length
      }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        console.log('PORT', port, 'STATUS', res.statusCode);
        console.log('BODY:\n', body);
        resolve();
      });
    });

    req.on('error', (err) => {
      console.error('PORT', port, 'ERROR', err.message);
      resolve();
    });

    req.write(pre);
    const stream = fs.createReadStream(filepath);
    stream.on('end', () => {
      req.write(post);
      req.end();
    });
    stream.pipe(req, { end: false });
  });
}

(async()=>{
  await post(5000);
  await post(8080);
})();
