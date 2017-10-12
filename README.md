# Impeachment Token Contracts and Tests

1. To run the tests please install `https://github.com/pipermerriam/populus`

2. Call `populus init` in your main project folder if you have not done already.

3. Call `populus compile` to compile the solidity contracts

3. Run py.test on the tests folder, please ensure that your **working directory** is the 
**project directory** and not the test directory


# SoulTokens Website

1. Install npm (js package manager) `https://www.npmjs.com/`

2. cd to **website** directory, install browserify globally: `(sudo) npm install --global browserify`

3. install ethjs-query and ethjs-contract locally `npm install --save 'ethjs-query` and
`npm install --save ethjs-contract`

4. Make sure your current working directory is still the **website** directory, and create the
bundle.js via `browserify js/soul.js -o js/bundle.js`


Note that there should be no development in bunlde.js, all changes should be done to
impeachment.js, and after each change `browserify js/soul.js -o js/bundle.js` needs to be
called to create a new bundle.


# Dockerized service

1. Build container in **project directory** via `docker build -t st-website:latest .`

2. Run container via `docker run -d -p 8080:80 st-website:latest`, website should now be available.