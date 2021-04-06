import responses
import spdkim


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
    assert response.status_code == 200


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
    assert response.status_code == 200


@responses.activate
def test_verifyDomain():
    apiKey = "fake-key"
    sendingDomain = "customer.domain"

    responses.add(
        responses.POST,
        "https://api.sparkpost.com/api/v1/sending-domains/" + sendingDomain + "/verify",
        status=200,
        content_type='application/json',
        body='{"results": "yay"}'
    )

    response = spdkim.verifyDomain(apiKey, sendingDomain)  # Test
    assert response.status_code == 200
