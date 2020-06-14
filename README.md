# Nike 30%

Sales sentinel for running shoes. Scrapes Running Warehouse and sends an email summary of new deals that fit the users' requirements (discount, price, model, sizes, etc.). Bringing back those Nike marketing dollars.

<p align="center">
<img src="assets/nike30.gif" alt="animated" />
</p>

## Getting Started

### Prerequisites

If you don't have geckodriver installed:
```
brew install geckodriver
```

Recommended:
```
brew install pipenv
```

### Installing

Clone the repository.
```
git clone https://github.com/bpenteado/nike30
```

Create a virtual environment. Pipenv recommended:
```
cd nike30
pipenv install
```

Set up user parameters. Example below.
```
vim params.json
```

Set up launch agent to run ``main.py``. [Tutorial here](https://davidhamann.de/2018/03/13/setting-up-a-launchagent-macos-cron/), example below.

## Examples

### Parameters

* `minDiscount`: minimum discount required to feature deal. 
    * (Float) in range [0.0, 1.0].
* `userSex`: user gender. 
    * (String) "M" or "F".
* `userSizes`: valid shoe sizes to be featured. US standards.
    * (Array) of 1-decimal floats, 0.5 increments.

**SMTP Configuration**: See [smtplib](https://docs.python.org/3/library/smtplib.html) for details.
* `login` and `pass`: SMTP server login credentials.
* `host`: SMTP server address.
* `port`: SMTP server port.

```json
{
"preferences": {
"minDiscount": 0.3,
"userSex": "M",
"userSizes": "[9.0, 9.5]"
},

"smtpParams" : {
"login":"*******@gmail.com",
"pass":"*******",
"host":"smtp.gmail.com",
"port": 587
}
}
```

### Launch Agent

* Example plist on ``com.nike30.scheduler.plist``.
* Example executable on ``launchd.fish``

## Deployment

Load agent:
```
launchtl bootstrap gui/<your-user-id> <your-plist-file>
```

Start agent:
```
launchtl kickstart -k gui/<your-user-id>/<your-plist-filename>
```


