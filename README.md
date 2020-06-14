# Nike 30%

Sales sentinel for running shoes. Scrapes Running Warehouse and sends an email summary of new deals that fit the users' requirements (discount, price, model, sizes, etc.). Bringing back those Nike marketing dollars.

![](assets/nike30.gif)


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
Set up launch agent. [Tutorial here](https://davidhamann.de/2018/03/13/setting-up-a-launchagent-macos-cron/), example plist below.

## Examples
### Parameters
### Plist

## Deployment
Load agent:
```
launchtl bootstrap gui/<your-user-id> <your-plist-file>
```
Start agent:
```
launchtl kickstart -k gui/<your-user-id>/<your-plist-filename>
```


