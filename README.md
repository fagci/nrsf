# Netrandom stalking framework (nrsf)

Netwotk research & automated information gathering framework. Without dependencies.
<img src="logo.png" align="right"></img>

## Usage

```
nrsf.py [-h] [--timeout TIMEOUT] [--limit LIMIT] [--workers WORKERS] [--debug DEBUG] modules [modules ...]

Netrandom stalking framework

positional arguments:
  modules

optional arguments:
  -h, --help         show this help message and exit
  --timeout TIMEOUT
  --limit LIMIT
  --workers WORKERS
  --debug DEBUG
```

## Gathered samples

FTP

```
[ftp] 172.xxx.110.xxx:21
{'DJI_0020.JPG'}
```

```
[ftp] 76.xxx.184.xxx:21
{'kraftwerk-greatest hits.jpg'}
```

```
[ftp] 185.xxx.150.xxx:21
{'Penguins.jpg'}
```

Quote of the day

```
[Qotd] 212.xx.90.xx:17
"Assassination is the extreme form of censorship."
 George Bernard Shaw (1856-1950)
```

```
[Qotd] 49.xxx.26.xxx:17
"A wonderful fact to reflect upon, that every human creature is constituted
 to be that profound secret and mystery to every other."
 Charles Dickens (1812-70)
```

```
[Qotd] 112.xxx.16.xxx:17
"We want a few mad people now. See where the sane ones have landed us!"
 George Bernard Shaw (1856-1950)
```

Time

```
[Time] 120.xx.171.xx:13
5:12:38 2020/12/30
```

```
[Time] 129.xxx.208.xxx:13
Monday, August 30, 2021 04:49:03-MET-DST
```

Telnet

```
[telnet(default strategy)] 80.xxx.xxx.xxx:23                                 
#
| LANCOM 1781AW                                                             
| Ver. 8.62.0050RU2 / 07.08.2012
| SN.  4002419818100978                                                     
| Copyright (c) LANCOM Systems
                                                                            
m3iHerbersJB, Connection No.: 002 (WAN)
```

```
[Telnet(default strategy)] 151.xxx.xxx.2:23
This is an unrestricted telnet server.
Please do not user for production purposes
```

HTTP

```
[Http] 78.xxx.xxx.xxx:80
Hello! Welcome to Synology Web Station!
```

```
[Http] 74.xxx.xxx.xxx:80
InMotion Hosting
```

```
[Http] 20.56.xxx.xxx:80
Your Azure Function App is up and running.
```

HTTPS

```
[https] 46.xxx.xxx.108:443
Toby Manley – Actor – London
```

```
[https] 35.xxx.xxx.53:443
MCEA news and affairs
```
