import pytest

from poetry_private_source_plugin.parsers import CodeArtifactParser
from poetry_private_source_plugin.parsers import SourceParserFactory


# Factory tests
@pytest.mark.parametrize(
    "valid_url",
    [
        "https://domain-12345.d.codeartifact.us-west-2.amazonaws.com/pypi/foo/bar",
        "https://subdomain-67890.d.codeartifact.eu-central-1.amazonaws.com/pypi/foo/bar",
    ],
)
def test_good_catch(valid_url):
    try:
        repo = SourceParserFactory(valid_url)
        assert isinstance(repo, CodeArtifactParser)
    except ValueError:
        pytest.fail("Valid URL raised ValueError")


@pytest.mark.parametrize(
    "invalid_url",
    [
        "https://invalid-url.com/",
        "https://domain-12345.d.s3.us-west-2.amazonaws.com/pypi/foo/bar"  # not codeartifact
        "https://domain.d.codeartifact.amazonaws.com/pypi/foo/bar",  # missing owner
        "https://12345.d.codeartifact.amazonaws.com/pypi/foo/bar",  # missing domain
        "https://subdomain-67890.d.codeartifact.eu-central-1.amazonaws.com/nvm/foo/bar",  # missing pypi
        "ftp://domain-12345.d.codeartifact.us-west-2.amazonaws.com/pypi/foo/bar",  # invalid protocol
    ],
)
def test_no_catch(invalid_url):
    with pytest.raises(ValueError, match="Given url does not follow any known repository pattern."):
        SourceParserFactory(invalid_url)


# Codeartifact tests
@pytest.mark.parametrize(
    "valid_url",
    [
        "https://domain-12345.d.codeartifact.us-west-2.amazonaws.com/pypi/foo/bar",
        "https://subdomain-67890.d.codeartifact.eu-central-1.amazonaws.com/pypi/pypi/foo/bar",
    ],
)
def test_valid_codeartifact_repository_url(valid_url):
    # Test that no exception is raised for valid URLs
    try:
        repo = CodeArtifactParser(valid_url)
        assert repo.url == valid_url
        assert repo.domain is not None
        assert repo.owner is not None
    except ValueError:
        pytest.fail("Valid URL raised ValueError")


@pytest.mark.parametrize(
    "invalid_url",
    [
        "https://invalid-url.com/",
        "https://domain-12345.d.s3.us-west-2.amazonaws.com/pypi/foo/bar"  # not codeartifact
        "https://domain.d.codeartifact.amazonaws.com/pypi/foo/bar",  # missing owner
        "https://12345.d.codeartifact.amazonaws.com/pypi/foo/bar",  # missing domain
        "https://subdomain-67890.d.codeartifact.eu-central-1.amazonaws.com/nvm/foo/bar",  # missing pypi
        "ftp://domain-12345.d.codeartifact.us-west-2.amazonaws.com/pypi/foo/bar",  # invalid protocol
    ],
)
def test_invalid_codeartifact_repository_url(invalid_url):
    # Test that a ValueError is raised for invalid URLs
    with pytest.raises(ValueError, match="Invalid codeartifact repository URL."):
        CodeArtifactParser(invalid_url)
