const request = require('request');
const cheerio = require('cheerio');
const fs = require('fs');

const startClip = "AUTHENTICITY CERTIFIED: Text version below transcribed directly from audio";
const startClip2 = "click for pdf";
const endClip = "Book/CDs by Michael E. Eidenmuller, Published by McGraw-Hill (2008)"
const endClip2 = "Copyright Status: Text = Public Domain. Audio = Restricted";

fs.readFile("obama_speeches_id.json", function(err, file) {
  /* something's wrong with the file */
  if (err) throw err;

  data = JSON.parse(file.toString());

  /* Slice here for testing */
  data.forEach(function(speech, i) {
    /**
     * Seems like the site doesn't want crawlers, we'll have to spoof some
     * headers for our needs
     */
    var options = {
      url: speech["link"],
      headers: {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'h2=o; he=llo',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'www.americanrhetoric.com',
        'Speech-Id': String(speech['id'])
      }
    }

    /**
     * Performing the actual request to the web page. If there's an error,
     * throw it. Else process it.
     */
    request(options, function(err, res, body) {
      if (err) throw err;
      if (res.statusCode == 200) {
        $ = cheerio.load(body);
        var text = $("td[align=center]").text();
        var passLvl1 = false;
        var passLvl2 = false;

        /* Cleaning the texts */
        text = text.replace(/\r\n/g, " ")
          .replace(/�/g, "'")
          .replace(/\s\s+/g, " ");

        // console.log(text);

        /* Check for this authenticity badge for easy clipping of text */
        if (text.indexOf(startClip) >= 0 && !passLvl1) {
          console.log("Got auth text");
          text = text.split(startClip)[1];
          passLvl1 = true;
        }
        if (text.indexOf(startClip2) >= 0 && !passLvl1) {
          console.log("Got pdf text");
          text = text.split(startClip2)[1];
          passLvl1 = true;
        }

        if (passLvl1) {

          /* "Book/CDs" text help to end the clipping */
          if (text.indexOf(endClip) >= 0 && !passLvl2) {
            console.log('Got Book/CDs text');
            text = text.split(endClip)[0];
            passLvl2 = true;
          }
          if (text.indexOf(endClip2) >= 0 && !passLvl2) {
            console.log('Got copyright status text');
            text = text.split(endClip2)[0];
            passLvl2 = true;
          }

          if (passLvl2) {
            console.log("Writing job file...");
            var sID = res.request.headers["Speech-Id"];
            fs.writeFile("raw/speech" + sID + ".txt", text.trim(), function(err) {
              if (err) throw err;
            })
          } else {
            console.log("Failed to restructure file")
            console.log(res.request.path);
          }
        }
      }
    });
  });
});
