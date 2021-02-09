known problems:
1. no error checking
   a. the artists I chose all had albums that were fully complete, so I have not implemented error checking
   b. not checking if authentication token expired (in progress in the authentication method)
2. Google Chrome
   a. autoplay does not work on Google Chrome (client side, Google Chrome blocking autoplay)
   
technical issues:
1. css not updating
   a. searched online in stackoverflow on issues with css not updating
   b. found in slack how to make it so c9 was not caching and using the cached file ever time the app ran
2. authentication returning error
   a. authenitcation token was working on Spotify preview, but not in app
   b. reading the spotify API documentation, you needed to send it in base64 encoded string to the API
   c. searched stack overflow and youtube on how to do authentications for Spotify API
   d. found youtube video detailing it and link to Github: https://github.com/codingforentrepreneurs/30-Days-of-Python/commit/9c8f45e840483133c340f10583ad6cb3f5e03fb6
