tetra ui
--------

This is a dashboard for tetra. It uses react, with npm to manage (certain)
dependencies.


quickstart
----------

First, install dependencies with npm and build the code:

    ### npm commands are run where package.json is located
    $ cd ./ui
    $ npm install
    $ npm run build

The tetra dashboard starts up with the rest of the docker containers. From the
root of this repository run:

    ### make commands are run where the makefile is located
    $ cd ..
    $ make docker-build
    $ make docker-dev

To find the location of the dashboard, run

    $ make docker-port

Then open up the dashboard in your browser.


commands
--------

To install npm dependencies (installed to `./node_modules/`):

    npm install

To compile jsx files into plain javascript, and bundle all that javascript into
one file (output to `./dist/tetra.bundle.js`):

    npm run build

To watch our `app/` dir for changes, and automatically rebuild everything:

    npm run autobuild

To add a new dependency, just for development (like build tools)

    npm install --save-dep <package-name>

To add a new dependency, for production (like react, bootstrap)

    npm install --save <package-name>


build process overview
----------------------

This goes over the many tools being used to build a simple webapp.

### npm

`npm` is the package manager and build tool for nodejs. Package metadata,
build steps, and dependencies are all stored in one `package.json` file.

##### managing npm modules

There are two different kinds of node modules we care about:

- `devDependencies` - things only needed for development. This includes build
tools, like `babel` and `webpack`.
- `dependendencies` - should only contain dependencies needed for production.

There are different ways to install a package, depending on how you want to
update `package.json`:

- `npm install <package>` - install a package to `./node_modules` but do not
update `package.json`
- `npm install --save-dev <package>` - install a package and add it to the
`devDependencies` in `package.json`
- `npm install --save <package>` - install a package and add it to the
`dependencies` in `package.json`

Node modules are always installed into `./node_modules/`, in the current
directory.

##### managing build steps

In `package.json` there is also a `scripts` field. This contains any steps
we want automated (similar to a makefile). The scripts can be run with
`npm run <script-name>`.

For example, if our `package.json` has:

    "scripts": {
        "do-a-thing": "echo 'hello'"
    }

Then we can do

    $ npm run do-a-thing

    > tetra-ui@1.0.0 do-a-thing /root/tetra/ui
    > echo 'hello'

    hello

### JSX (with babel)

React allows us to write JavaScript and HTML (approximately) together in
[.jsx](https://facebook.github.io/react/docs/jsx-in-depth.html) files. A build
step is required to convert jsx to plain js files. This build step is performed
by [babel](https://babeljs.io/).

When you invoke `npm run build`, babel compiles the jsx and outputs js files to
`./dist/`.

Aftering running `npm install`, you can also run babel directly:

    ./node_modules/.bin/babel build app -d dist

### JavaScript Modules (with webpack)

(not to be confused with node modules)

Babel _also_ supports
[ECMAScript 6](https://babeljs.io/docs/learn-es2015/), which specifies new
features for JavaScript-like scripting languages. Since ECMAScript 6 is not
fully supported by all browsers, the idea is that Babel compiles your code
using these new features to plain JavaScript that works on all browsers.

One of these features is modules, which lets us write code like:

    import React from 'react';

Babel compiles import statements to different statements that a bundler can
understand. The bundler reads the imports, finds all the dependent js files,
and merges them into one, unified js file. We then include this single js file
in our html.

In our case, the bundler is [webpack](https://webpack.github.io/). When you
invoke `npm run build`, babel will run first, followed by webpack. Webpack
spits out `tetra.bundle.js`. Then in our index.html, we include the bundled
javascript,

    <script src="/dist/tetra.bundle.js"></script>
