What to install:
1. pip install beautifulsoup4
2. pip install python-dotenv

known problems:
1. no error checking
   a. the artists I chose all had albums that were fully complete, so I have not implemented error checking
   b. for future, I can check to see if the song being returned is not an empty string, if it is, find another song
2. Google Chrome
   a. autoplay does not work on Google Chrome (client side, Google Chrome blocking autoplay)
   b. no current workaround present other than use a different browser
3. Song lyrics sometimes not being displayed correctly from Genius
   a. Genius does not have the song sometimes
   b. current temp fix is link to search results of the song
   c. if lyrics are displayed correctly, link is direct to lyrics page
   
technical issues:
1. css not updating
   a. searched online in stackoverflow on issues with css not updating
   b. found in slack how to make it so c9 was not cacheing and using the cached file ever time the app ran
2. authentication returning error
   a. authenitcation token was working on Spotify preview, but not in app
   b. reading the spotify API documentation, you needed to send it in base64 encoded string to the API
   c. searched stack overflow and youtube on how to do authentications for Spotify API
   d. found youtube video detailing it and link to Github: https://github.com/codingforentrepreneurs/30-Days-of-Python/commit/9c8f45e840483133c340f10583ad6cb3f5e03fb6
3. text overflow on website
   a. lyrics being displayed on the website were sometimes too much
   b. find a way to either scroll through lyrics or cut them short
   c. searched how to create text scroll box in HTML
   d. found https://www.quackit.com/html/codes/html_scroll_box.cfm
