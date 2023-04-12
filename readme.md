# SMTP Server Parser
The SMTP Server Parser is a python based smtp server that can be used to check incoming emails for various properties, such as SPF and DKIM verification, before accepting them. It can also send the email to a webhook, or print it to the console, depending on the configuration.

There are advance options as well with addon scripts that can do custom parsing or sending.

https://github.com/Sumiza/smtp-parser


## Docker Hub Tags
To keep the dependencies up to date a new build is made daily and tagged as latest, if you want to lock into a specific build use the date or commit hash. Or use  the master tag to only update when there is a change to the code.

- `latest` : Updated daily and when a new build is done
- `master` : Updated when a new build is done
- `date` : Daily build
- `commit hash` : Github commit build

## Environment Variables
The following environment variables can  be set to configure the SMTP server:

- `HOST`: The IP address or hostname to bind the SMTP server to. Defaults to `0.0.0.0`.
- `PORT`: The port number to bind the SMTP server to. Defaults to `25`.
- `TARGET_EMAIL`: An optional email address to filter incoming emails by. If set, the SMTP server will only accept emails that are addressed to this email address.
- `SOURCE_EMAIL`: An optional email address to filter incoming emails by. If set, the SMTP server will only accept emails that are sent from this email address.
- `SPF_ALLOW_LIST`: An optional JSON-formatted string containing a list of allowed SPF responses `['pass', 'permerror', 'fail', 'temperror', 'softfail', 'none', 'neutral' ]`.
- `DKIM_REJECT`: An optional boolean value indicating whether to reject emails that fail DKIM verification. If set to anything, any email that fails DKIM verification will be rejected. If not set, emails will not be rejected based on DKIM verification.
- `IDENT`: An optional string that will be used as the identity string for the SMTP server. Defaults to an empty string.
- `EMAIL_SIZE`: An optional integer value indicating the maximum size of an incoming email, in bytes. Defaults to `5048576`.
- `LOG_OFF`: An optional boolean value indicating whether to disable console logging. If set to `True`, console logging will be disabled. If not set, or set to any other value, console logging will be enabled.
- `WEBHOOK_URL`: An optional string containing the URL of a webhook to send incoming emails to. If set, the SMTP server will send incoming emails to this webhook.
- `WEBHOOK_HEADERS`: An optional JSON-formatted string containing a dictionary of headers to include in the webhook request. If set, the headers in this dictionary will be added to the webhook request.
- `HMAC_SECRET`: An optional string containing a secret key to use for HMAC validation of the webhook request. If set, the webhook request will include an HMAC signature for validation.
- `PIP_INSTALL`: An optional string containing any projects you need to download with pip for addon scripts `'webhookbin urlrequest secondstotext'`

## Usage
To use the smtp server, simply run the Python script or docker container. The SMTP server will bind to the specified host and port and begin accepting incoming emails.

Incoming emails will be checked for SPF and DKIM verification, and filtered according to the configuration specified in the environment variables. If an incoming email passes all checks, it will be sent to the webhook URL specified in the environment variables, or printed to the console, depending on the configuration.

## Dependencies

- Python 3.7 or higher
- The spf package
- The requests package
- The aiosmtpd package
- The dkim package

## Advance Options
Todo

### Custom addon scripts
Todo

### Script Examples
Todo
