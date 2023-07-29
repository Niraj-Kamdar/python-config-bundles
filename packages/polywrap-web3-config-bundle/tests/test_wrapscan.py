from polywrap_client import PolywrapClient
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from polywrap_core import Uri
from polywrap_http_plugin import http_plugin
from polywrap_sys_config_bundle import BundlePackage
from polywrap_uri_resolvers import ExtendableUriResolver

from polywrap_web3_config_bundle.embeds import get_embedded_wrap


ipfs_providers = [
    "https://ipfs.wrappers.io",
    "https://ipfs.io",
]


def test_wrapscan_min_resolver():
    bundle = {
        "http": BundlePackage(
            uri=Uri.from_str("plugin/http@1.1.0"),
            package=http_plugin(),
            implements=[
                Uri.from_str("ens/wraps.eth:http@1.1.0"),
                Uri.from_str("ens/wraps.eth:http@1.0.0"),
            ],
            redirects_from=[
                Uri.from_str("ens/wraps.eth:http@1.1.0"),
                Uri.from_str("ens/wraps.eth:http@1.0.0"),
            ],
        ),
        "http_resolver": BundlePackage(
            uri=Uri.from_str("embed/http-uri-resolver-ext@1.0.1"),
            package=get_embedded_wrap("http-resolver"),
            implements=[
                Uri.from_str("ens/wraps.eth:http-uri-resolver-ext@1.0.1"),
                *ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS,
            ],
            redirects_from=[
                Uri.from_str("ens/wraps.eth:http-uri-resolver-ext@1.0.1"),
            ],
        ),
        "wrapscan_resolver": BundlePackage(
            uri=Uri("https", "wraps.wrapscan.io/r/polywrap/wrapscan-uri-resolver@1.0"),
            implements=[
                Uri.from_str("wrapscan.io/polywrap/wrapscan-uri-resolver@1.0"),
                *ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS,
            ],
            redirects_from=[
                Uri.from_str("wrapscan.io/polywrap/wrapscan-uri-resolver@1.0")
            ],
        ),
        "ipfs_http_client": BundlePackage(
            uri=Uri.from_str("embed/ipfs-http-client@1.0.0"),
            package=get_embedded_wrap("ipfs-http-client"),
            implements=[Uri.from_str("ens/wraps.eth:ipfs-http-client@1.0.0")],
            redirects_from=[Uri.from_str("ens/wraps.eth:ipfs-http-client@1.0.0")],
        ),
        "ipfs_resolver": BundlePackage(
            uri=Uri.from_str("embed/sync-ipfs-uri-resolver-ext@1.0.1"),
            package=get_embedded_wrap("ipfs-sync-resolver"),
            implements=[
                Uri.from_str("ens/wraps.eth:sync-ipfs-uri-resolver-ext@1.0.1"),
                *ExtendableUriResolver.DEFAULT_EXT_INTERFACE_URIS,
            ],
            redirects_from=[
                Uri.from_str("ens/wraps.eth:sync-ipfs-uri-resolver-ext@1.0.1"),
            ],
            env={
                "provider": ipfs_providers[0],
                "fallbackProviders": ipfs_providers[1:],
                "retries": {"tryResolveUri": 2, "getFile": 2},
            },
        ),
    }

    builder = PolywrapClientConfigBuilder()
    for package in bundle.values():
        package.add_to_builder(builder)

    config = builder.build()
    client = PolywrapClient(config)

    response = client.try_resolve_uri(
        Uri.from_str("wrapscan.io/polywrap/wrapscan-uri-resolver@1.0")
    )

    print(response)
    assert response is None