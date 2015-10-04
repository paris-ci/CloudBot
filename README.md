[![Build Status](https://travis-ci.org/paris-ci/CloudBot.svg?branch=master)](https://travis-ci.org/paris-ci/CloudBot)
[![Coverage Status](https://coveralls.io/repos/paris-ci/CloudBot/badge.svg?branch=master&service=github)](https://coveralls.io/github/paris-ci/CloudBot?branch=master)

# CloudBot

CloudBot is a simple, fast, expandable open-source Python IRC Bot!

## Getting CloudBot

This is my fork of cloudbot. For the official version, see [This github project](https://github.com/CloudBotIRC/CloudBot/).

## Installing CloudBot

Firstly, CloudBot will only run on **Python 3.4 or higher**. Because we use the asyncio module, you will not be able to use any other versions of Python.

To install CloudBot on *nix (linux, etc), see [here](https://github.com/CloudBotIRC/CloudBot/wiki/Installing-on-*nix)

To install CloudBot on Windows, see [here](https://github.com/CloudBotIRC/CloudBot/wiki/Installing-on-Windows)


### Running CloudBot

Before you run the bot, rename `config.default.json` to `config.json` and edit it with your preferred settings. You can check if your JSON is valid using [jsonlint.com](http://jsonlint.com/)!

Once you have installed the required dependencies and renamed the config file, you can run the bot! Make sure you are in the correct folder and run the following command:

```
python3.4 -m cloudbot
```

Note that you can also run the `cloudbot/__main__.py` file directly, which will work from any directory.
```
python3.4 CloudBot/cloudbot/__main__.py
```
Specify the path as /path/to/repository/cloudbot/__main__.py, where `cloudbot` is inside the repository directory.

## Getting help with CloudBot

### Documentation

The documentation is crapy. You should'nt use it...

More at the [Wiki Main Page](https://github.com/CloudBotIRC/CloudBot/wiki).

### Support

The developers reside in [#CloudBot](irc://irc.esper.net/cloudbot) on [EsperNet](http://esper.net) and would be glad to help you.
I reside in #himself in esper too !

## Example CloudBots

You can find a number of example bots in [#CloudBot](irc://irc.esper.net/cloudbot "Connect via IRC to #CloudBot on irc.esper.net").

## Changelog

See every commits I did...

## License

CloudBot is **licensed** under the **GPL v3** license. The terms are as follows.

![GPL V3](https://www.gnu.org/graphics/gplv3-127x51.png)
    
    CloudBot

    Copyright © 2011-2015 Luke Rogers / CloudBot Project

    CloudBot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CloudBot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CloudBot.  If not, see <http://www.gnu.org/licenses/>.
    
This product includes GeoLite2 data created by MaxMind, available from
<a href="http://www.maxmind.com">http://www.maxmind.com</a>. GeoLite2 databases are distributed under the [Creative Commons Attribution-ShareAlike 3.0 Unported License](https://creativecommons.org/licenses/by-sa/3.0/)

![Powered by wordnik](https://www.wordnik.com/img/wordnik_badge_a1.png)

This product uses data from <a href="http://wordnik.com">http://wordnik.com</a> in accordance with the wordnik.com API <a href="http://developer.wordnik.com/#!/terms">terms of service</a>.
