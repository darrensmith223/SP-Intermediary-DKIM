import responses
from spdkim import spdkim


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
    response = spdkim.addIntermediaryDomain(apiKey, intermediaryDomain)  # Test
    assert response == 'yay'


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

    response = spdkim.addSendingDomain(apiKey, sendingDomain)  # Test
    assert response == 'yay'


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

    response = spdkim.verifyDomain(apiKey, sendingDomain)  # Test
    assert response == 'yay'
