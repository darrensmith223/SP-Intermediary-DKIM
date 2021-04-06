# SP-Intermediary-DKIM

## Overview
As an email service provider, there are many different priorities and considerations that you are factoring, especially when starting out, and one of the most important is for your customers to have an easy onboarding experience.  You want your customers to successfully set up their integration with your platform with as few barriers as possible, and you want these messages to perform well so that your customers have as positive of an experience as possible when sending through your platform.

When it comes to onboarding a customer onto your platform, Email Service Providers want:

* Their customer to be able to use their own domain when sending messages through the platform for brand alignment
* To implement an easily understood onboarding process with as few steps as possible
* To ensure the messages successfully pass DKIM upon delivery for the best customer experience


With SparkPost, creating a frictionless onboarding experience for your customers can be accomplished by using an intermediary domain that you manage, which your customers then CNAME to.  This allows for a streamlined setup process that is consistent for each customer, and can be easily documented, communicated in advance, and performed in parallel with other onboarding steps.

Using an intermediary domain for DKIM enables a customer to successfully send from your platform using their domain with only one step - add a CNAME record pointing to a predetermined domain.  This can be implemented into your onboarding process by communicating to your customers in advance they should create the CNAME record.  

Ex: "Add CNAME `xyz._domainkey.<your.domain>` that points to `xyz._domainkey.<platform.domain>`."


# Using SP-Intermediary-DKIM

The primary script in SP-Intermediary-DKIM is `SPDKIM.py`, with three primary functions:
* `addIntermediaryDomain()` - Generates a 1024 bit private and public key pair, and then adds the intermediary domain to your SparkPost account using the generated key pair.
* `addSendingDomain()` - Adds your customer sending domain to your SparkPost account using the same private and public key pair generated for your intermediary domain.
* `verifyDomain()` - DKIM verfies a domain in your SparkPost account.

An example process would be to:

1. Add the intermediary domain to your SparkPost account with `addIntermediaryDomain`
2. Update your DNS with the TXT record displayed in your SparkPost account.
3. DKIM verify your intermediary domain with `verifyDomain`.
4. Instruct your customers to add a predefined CNAME record to their DNS that will point to your intermediary domain.

"Ex: Add CNAME `xyz._domainkey.<your.domain>` that points to `xyz._domainkey.<platform.domain>`."

6. Add your customer's sending domain to your SparkPost account with `addSendingDomain`
7. DKIM verify your customer's sending domain with `verifyDomain`


## Generate Key Pair and Add Intermediary Domain

To generate a key pair for your intermediary domain and then add the domain to your SparkPost account, you will use the function `addIntermediaryDomain`.  This will generate a 1024 bit key pair. `addIntermediaryDomain` has the following parameters:

addIntermediaryDomain(apiKey, domain, outputPath=None, selector=None)
* apiKey: Your SparkPost API key.
* domain:  The intermediary domain that will be added to your SparkPost account.
* outputPath:  (optional) The local path used to store the DKIM key pair locally.  Defaults to current working directory.
* selector:  (optional) The selector used for the DKIM record.  Defaults to "scphMMYY" where MMYY represents the current month and year.

An example of adding an intermediary domain to your SparkPost account can be found below:

```Python


import spdkim

# Initialize Variables
apiKey = "SPARKPOST_API_KEY"
intermediaryDomain = "intermediary.domain"

spdkim.addIntermediaryDomain(apiKey, intermediaryDomain)  # Add Intermediary Domain to SparkPost Account
```


## Add Customer Sending Domains

To add a customer sending domain to your SparkPost account, you will use the function `addSendingDomain`, which will use the same key pair generated in `addIntermediaryDomain` when adding the intermediary domain.  `addSendingDomain` has the following parameters:

addSendingDomain(apiKey, domain, outputPath=None, selector=None)
* apiKey:  Your SparkPost API Key.
* domain:  Your customer's sending domain that will be added to your SparkPost account.
* outputPath:  (optional)  Local path where the key pair is stored.  Defaults to current working directory.
* selector:  (optional) The selector used for the DKIM record.  Defaults to "scphMMYY" where MMYY represents the current month and year.

An example of adding your customer's domain can be found below:

```Python


import spdkim

# Initialize
apiKey = "SPARKPOST_API_KEY"
sendingDomain = "customer.domain"

spdkim.addSendingDomain(apiKey, sendingDomain)  # Add Customer Sending Domain to SparkPost Account
```

Instruct your customers to add a predefined CNAME record to their DNS that will point to your intermediary domain.
_Ex: Add CNAME xyz._domainkey.<your.domain> that points to xyz._domainkey.<platform.domain>._


## Verify Domains

To DKIM verify both the intermediary domain and your customer sending domains, you will use the function `verifyDomain`, which will make an API call to SparkPost and prompt SparkPost to verify DNS has been successfully updated with the correct DKIM records.  This enables the sending domain to be used for sending messages through SparkPost, and ensures that any messages sent from this domain will successfully pass DKIM authentication.

`verifyDomain` has the following parameters:

verifyDomain(apiKey, domain)
* apiKey:  Your SparkPost API Key.
* domain:  The domain that will be DKIM verified.  This can be either your intermediary domain or your customer's domain.

An example of verifying your customer's sending domain can be found below:

```Python


import spdkim

# Initialize
apiKey = "SPARKPOST_API_KEY"
sendingDomain = "customer.domain"

spdkim.verifyDomain(apiKey, sendingDomain)  # Verify Customer Domain on SparkPost Account
```
