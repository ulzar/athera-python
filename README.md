# athera-python
Welcome Atherians! This is the Python wrapper around the Athera API.

## Authenticating
See [here](https://docs.athera.io/api/athera-api.html) for the full API documentation, including how to generate a Client ID and Client Secret via the [Developer Dashboard](https://developer.athera.io/).

Once you have a Client ID and Secret, Linux and OSX users can perform the following steps to generate the (JWT) token that all requests to the Athera API require for authentication:

```
export ATHERA_API_CLIENT_ID=<client_id>
export ATHERA_API_CLIENT_SECRET=<client_secret>
export PYTHONPATH=<path_to_athera-python>
cd athera/auth
./generate_jwt.sh
```

Windows users should be able to improvise by setting the environment variables described above, setting up the python environment in `athera/auth/requirements.txt` (virtual environment recommended) and running `python ./athera/auth/generate_jwt.py`.

Running the script provides a URL which when clicked, or pasted into a browser, walks you through the OAuth process. The script outputs a JWT token.

Generating a token needs to be done only once, then when the token expires. Tokens can be refreshed to prevent expiry. See the `athera.auth.generate_py.refresh_token` function for details on how to do this.

## Using Athera Python
To use the Athera API python wrappers in your own projects, add the following to your python requirements file and install into your virtualenv:

```
git+git://github.com/athera-io/athera-python.git@master
six
requests
grpcio
protobuf
```

You should then be able to do, for example:

```python
from athera.api import get_orgs
orgs = get_orgs("<base_url>", "<token>")
```

base_url is a constant:

`https://api.athera.io/api/v1`

It is provided as an argument to function calls to allow for future flexibility.

## File sync
Data I/O between local storage and Athera storage is now possible. The Athera Sync API uses [gRPC](https://grpc.io/) to perform bi-directional data transfer.

We provide a Sync client in `athera.sync.client` which you should use to manage transfers. This client requires the JWT as above, plus also a region string, one of:

* `us-west1`
* `europe-west1`
* `australia-southeast1`

### Why is a region required?
When you perform an upload, the uploaded file gets automatically cached into the target region. It will eventually get written into the external storage bucket, if applicable. Other regions need to do a storage rescan operation to detect the newly arrived file.

You can actually use Athera Sync API to upload to or download from your own buckets that you've connected to Athera!

## Examples
See the examples folder for a few simple scripts which use the api to query your Athera contexts. The examples folder has its own requirements.txt.

## Tests
An alternative source of implementation specifics is the test folder. You'll be unlikely to be able (or want to) run the tests as many environment variables are required (see `athera-python/.test.settings`).

The tests are used by us to check for regressions and core Athera functionality, but are provided here for your reference.

## Contributions
Contributions are very welcome. Email contact@athera.io to be granted write access to the repository.

_Team Athera_
