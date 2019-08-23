# Socket Protocol

## Basic Protocol

The protocol has a max of 36 different commands, but as of now only 2 are used, the protcol consists of the first character being the command, and the rest comma seperated values between parameters

eg. `cP1,P2,P3,...`

## Registering 

Command: `r[key],[default],[description]`

### Register Example

Request: `rHello,World,The hello world config option`

Response: `OK`

## Getting

Command: `g[key]`

### Get Example

Request: `gHello`

Response: `World`