# R53_Upserter
This project is a python script that updates a route53 based A record to the public ip address of the host running the script through the use of the AWS api.

## Environment variables
The script uses 4 environment variables:

| Variable              | Required?     | Description|
| -------------         |:-------------:| -----:|
| AWS_ACCESS_KEY_ID     | required      | Specifies an AWS access key associated with an IAM user or role. |
| AWS_SECRET_ACCESS_KEY | required      | Specifies the secret key associated with the access key. This is essentially the "password" for the access key. |
| A_RECORD              | required      | The a record you wish to create or update, example: record.domain.com |
| INTERVAL              | optional      | The interval in seconds at which the update occurs, default is 900 seconds, or 15 minutes |
| IP_URL              | optional      | The url used for determining local IP, defaults to "icanhazip.com", when using alternatives, please ensure the ip returned is IPv4 and only returns a clean octet with no qoutes or "end of line" characters |

Set the environment variables in a way that is appropriate for your operating system.

Example:

Linux/MacOS
```shell
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
export INTERVAL=300
export A_RECORD=record.domain.com
```
[More information.](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)

## Running the script manually
Set the environment variables as explained, run the script using python3
```shell
python3 r53_upserter.py
```

## Docker
For your convenience a dockerfile is provided.
### Manual build
run docker build in the root of this repo.
```shell
docker build -t r53_upserter .
```
### Premade docker image
This docker image is prebuild and available on duckerhub.
Pull from dockerhub:
```shell
docker pull martyca/r53_upserter
```
### Run container
Run the container setting the required environment variables:
```shell
 docker run -d \
  -e A_RECORD \
  -e AWS_ACCESS_KEY_ID\
  -e AWS_SECRET_ACCESS_KEY\
  -e INTERVAL\
  martyca/r53_upserter
 ```