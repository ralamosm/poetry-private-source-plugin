import os
import re

import boto3
from furl import furl


class BaseParser:
    """Base class for all kind of parsers"""

    def __init__(self, url):
        f = furl(url)
        f.path.normalize()
        self.url = f.url

    @property
    def username(self):
        pass

    @property
    def password(self):
        pass


class CodeArtifactParser(BaseParser):
    """Parser recognizing codeartifact repos"""

    # https://domain-owner.d.codeartifact.region.amazonaws.com/pypi/repo-name/simple/

    def __init__(self, url):
        super().__init__(url)

        rx = re.compile(r"^https://(?P<domain>[-_\w]+)-(?P<owner>\d+)\.d\.codeartifact\.(?:[-\w]+)\.amazonaws.com/pypi/", re.I)
        m = rx.search(self.url)
        if not m:
            raise ValueError("Invalid codeartifact repository URL.")

        self.domain = m.group("domain")
        self.owner = m.group("owner")
        self.token_ttl = int(os.getenv("POETRY_CODEARTIFACT_TOKEN_TTL", 900))

    @property
    def username(self):
        return "aws"

    @property
    def password(self):
        return boto3.client("codeartifact").get_authorization_token(domain=self.domain, domainOwner=self.owner, durationSeconds=self.token_ttl)[
            "authorizationToken"
        ]


def SourceParserFactory(url):
    for cls in (CodeArtifactParser,):
        try:
            return cls(url)
        except ValueError:
            pass
    raise ValueError("Given url does not follow any known repository pattern.")
