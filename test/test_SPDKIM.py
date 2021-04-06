import SPDKIM
import responses


@responses.activate
def test_addIntermediaryDomain():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/sending-domains',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    apiKey = "fake-key"
    intermediaryDomain = "intermediary.domain"
    SPDKIM.addIntermediaryDomain(apiKey, intermediaryDomain)  # Test


@responses.activate
def test_addCustomerDomain():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/sending-domains',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    apiKey = "fake-key"
    sendingDomain = "customer.domain"

    SPDKIM.addSendingDomain(apiKey, sendingDomain)  # Test


@responses.activate
def test_verifyDomain():
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/sending-domains',
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    apiKey = "fake-key"
    sendingDomain = "customer.domain"

    SPDKIM.verifyDomain(apiKey, sendingDomain)  # Test
