# athera-python
Welcome Atherians! This is the Python wrapper around the Athera API.

## Authenticating
See [here](https://docs.athera.io/api/athera-api.html) for the full API documentation, including how to generate a Client ID and Client Secret via the [Developer Dashboard](https://developer.athera.io/).

Once you have a Client ID and Secret, Linux and OSX users can perform the following steps to generate the (JWT) token that all requests to the Athera API require for authentication:

```
export ATHERA_API_CLIENT_ID=<client_id>
export ATHERA_API_CLIENT_SECRET=<client_secret>
cd auth
./generate_jwt.sh
```

Windows users should be able to improvise by setting the environment variables described above, setting up the python environment in `auth/requirements.txt` (virtual environment recommended) and running `python ./auth/generate_jwt.py`.

Running the script provides a URL which when clicked, or pasted into a browser, walks you through the OAuth process. The script outputs a JWT token.

Generating a token needs to be done only once, then when the token expires. Tokens can be refreshed to prevent expiry. See the auth.generate_py.refresh_token function for details on how to do this.

## Using Athera Python
To use the Athera API python wrappers in your own projects, add the following to your python requirements file and install into your virtualenv:

```
requests
git+git://github.com/athera-io/athera-python.git@v0.1
```

You should then be able to do, for example:

```python
from athera.api import get_orgs
orgs = get_orgs("<base_url>", "<token>")
```

base_url is a constant:

`https://api.athera.io/api/v1/`

It is provided as an argument to function calls to allow for future flexibility.

## File sync
Data I/O between local storage and Athera storage is in progress and will be added in a future release.

## Contributions
Contributions are very welcome. Email contact@athera.io to be granted write access to the repository.

_Team Athera_
