from pyff.samlmd import parse_saml_metadata
from pyff.utils import unicode_stream

from met.metadataparser.tests import TestCase


class XMLParserTestCase(TestCase):

    def test_xml_namespaces(self):
        xml = '''
          <EntitiesDescriptor xmlns="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:mdrpi="urn:oasis:names:tc:SAML:metadata:rpi" xmlns:mdui="urn:oasis:names:tc:SAML:metadata:ui" xmlns:shibmd="urn:mace:shibboleth:metadata:1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ID="FEDURUS-20210726080001" Name="urn:mace:fedurus.ru" validUntil="2021-08-22T08:00:01Z" xsi:schemaLocation="urn:oasis:names:tc:SAML:2.0:metadata saml-schema-metadata-2.0.xsd urn:mace:shibboleth:metadata:1.0 shibboleth-metadata-1.0.xsd urn:oasis:names:tc:SAML:metadata:ui saml-metadata-ui-1.0.xsd http://www.w3.org/2000/09/xmldsig# xmldsig-core-schema.xsd">
            <ds:Signature>
              <ds:SignedInfo>
                <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
                <ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
                <ds:Reference URI="#FEDURUS-20210726080001">
                  <ds:Transforms>
                    <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
                    <ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
                  </ds:Transforms>
                  <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
                  <ds:DigestValue>D8gr8j5mMQlb9nYHAQl5T4tz6euIRp5OIF14QOCzHPo=</ds:DigestValue>
                </ds:Reference>
              </ds:SignedInfo>
              <ds:SignatureValue> frUpVg2WIu/PkiQ6IzeOwURPQhnj4nT/VETBfR5venPhoF7dIAJBHYqU7h4R7UOz0FSyidaAKhp+ qsCX9ebRWfrhhNDq8/wUQA7ZLA/Pj7/RKk5MJCymVX+qogw2rkAZrIo2CvuKxxCdh895zPi+YRrj XZq2kilm0ZTidLNHZbOTY9zCpZLIGdOe30VVk8a740c6tXhOFoNCMQ4GLppBdbPIsXidH9Fv4+WA uuqM/TtH3P7LnAwp3n9yzY7+ErofScopUlR2kN1feYh1gOs8MLP4J0JQ0wZ8MA2Tn3dpRv77dpz4 z0pEsBBoatPn7HjrvNrfHotNBVkpmuaTaqvzWA== </ds:SignatureValue>
              <ds:KeyInfo>
                <ds:KeyValue>
                  <ds:RSAKeyValue>
                    <ds:Modulus> ra4CF2p2Ne1i9Hq63g/jOJSfhOY/uko+1e2KrN0HC7BjH6tu+M8uJ4WHt/2Wq9VanEIX9jZQQoCS O0t+x4GwFbGpkLoEZpTMRGdDUe95s8GeOeXNxKXQ9Z8ET9WKd9sLkzuwXVzLuLqbwsph6rPkXsrL ILAWcy7cSXcX5ZoWpU1xvrfqamxb3dxaGChsjY1oQE6otO/kS5h4WLdR4gHOzkVdAVi4a0HwPw5/ ehlFAWDdH2EE2SqY6SS7AkjitmV08OacMyB6FZJlURMjVCrH50FBhpEKIpP0XDHkn6Q98r42FIqC QgpqHRV5KUoI1CTJJoD8pBN/xxIQsgbivP+A9w== </ds:Modulus>
                    <ds:Exponent>AQAB</ds:Exponent>
                  </ds:RSAKeyValue>
                </ds:KeyValue>
                <ds:X509Data>
                  <ds:X509Certificate> MIIEfTCCA2WgAwIBAgIJAPLDYeYrUGvgMA0GCSqGSIb3DQEBBQUAMIGFMQswCQYDVQQGEwJSVTEZ MBcGA1UECBMQU2FpbnQtUGV0ZXJzYnVyZzEZMBcGA1UEBxMQU2FpbnQtUGV0ZXJzYnVyZzEQMA4G A1UEChMHZkVEVXJ1czEZMBcGA1UECxMQTWV0YWRhdGEgc2lnbmluZzETMBEGA1UEAxMKZmVkdXJ1 cy5ydTAeFw0xMzEyMTIxMzAyNTNaFw0yMzEyMTAxMzAyNTNaMIGFMQswCQYDVQQGEwJSVTEZMBcG A1UECBMQU2FpbnQtUGV0ZXJzYnVyZzEZMBcGA1UEBxMQU2FpbnQtUGV0ZXJzYnVyZzEQMA4GA1UE ChMHZkVEVXJ1czEZMBcGA1UECxMQTWV0YWRhdGEgc2lnbmluZzETMBEGA1UEAxMKZmVkdXJ1cy5y dTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAK2uAhdqdjXtYvR6ut4P4ziUn4TmP7pK PtXtiqzdBwuwYx+rbvjPLieFh7f9lqvVWpxCF/Y2UEKAkjtLfseBsBWxqZC6BGaUzERnQ1HvebPB njnlzcSl0PWfBE/VinfbC5M7sF1cy7i6m8LKYeqz5F7KyyCwFnMu3El3F+WaFqVNcb636mpsW93c WhgobI2NaEBOqLTv5EuYeFi3UeIBzs5FXQFYuGtB8D8Of3oZRQFg3R9hBNkqmOkkuwJI4rZldPDm nDMgehWSZVETI1Qqx+dBQYaRCiKT9Fwx5J+kPfK+NhSKgkIKah0VeSlKCNQkySaA/KQTf8cSELIG 4rz/gPcCAwEAAaOB7TCB6jAdBgNVHQ4EFgQU7rZT86DIU+yS/Q8G2144Nx3KougwgboGA1UdIwSB sjCBr4AU7rZT86DIU+yS/Q8G2144Nx3KouihgYukgYgwgYUxCzAJBgNVBAYTAlJVMRkwFwYDVQQI ExBTYWludC1QZXRlcnNidXJnMRkwFwYDVQQHExBTYWludC1QZXRlcnNidXJnMRAwDgYDVQQKEwdm RURVcnVzMRkwFwYDVQQLExBNZXRhZGF0YSBzaWduaW5nMRMwEQYDVQQDEwpmZWR1cnVzLnJ1ggkA 8sNh5itQa+AwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOCAQEAhKFTu53CO9Tlq7U2hNal UiPQ1vLc8lel0+jW4cIIKgxO7/NW/sG9Ly6QgTmkId2PEEFOwySxiOER2pZMXJ8LvIrKcXvzDgl3 5R6/0Dbt6nyCgFqCkE4il50tE3GnZ8fCjt/KDtymgr9vNODytRrztZlkfQWhtDiCYHnbEEiw3eKv +O/8Sjdz+SGoXY2l2opdebQEewWsdG71O2LJCbH7DzIozrC3wB1Q9IfiFTqzLXqpAzPlewFN6IRg vrQmcfMz0LA3i6I8QQEFDLFiFnm2aCUpHDur4EJt2M/Mpy86a4s3NuiMBlxf2OaljB5xr3uh+ltH y7pVABolilVbdezWcw== </ds:X509Certificate>
                </ds:X509Data>
              </ds:KeyInfo>
            </ds:Signature>
            <EntityDescriptor entityID="https://auth.antiplagiat.ru/Saml2">
              <SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
                <Extensions>
                  <mdui:UIInfo>
                    <mdui:DisplayName xml:lang="en">Antiplagiat</mdui:DisplayName>
                    <mdui:DisplayName xml:lang="ru">Антиплагиат</mdui:DisplayName>
                    <mdui:Description xml:lang="en">Service for plagiarism detection in text documents.</mdui:Description>
                    <mdui:Description xml:lang="ru">Сервис поиска текстовых заимствований.</mdui:Description>
                    <mdui:InformationUrl xml:lang="ru">https://www.antiplagiat.ru/</mdui:InformationUrl>
                    <mdui:InformationUrl xml:lang="en">https://www.antiplagiat.com/</mdui:InformationUrl>
                    <mdui:Logo height="33" width="88">https://auth.antiplagiat.ru/img/logo.png</mdui:Logo>
                  </mdui:UIInfo>
                </Extensions>
                <KeyDescriptor>
                  <ds:KeyInfo>
                    <ds:X509Data>
                      <ds:X509Certificate>
                MIIDWzCCAkOgAwIBAgIQVHEHqm/cq75MLnmYAGGVlzANBgkqhkiG9w0BAQUFADAeMRwwGgYDVQQDDBNhdXRoLmFudGlwbGFnaWF0LnJ1MB4XDTE5MDkxODE0NTQyMFoXDTIwMDkxODE1MTQyMFowHjEcMBoGA1UEAwwTYXV0aC5hbnRpcGxhZ2lhdC5ydTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALtF4MBRFzyVH/piQGqzNGuAmV1y+hlscUVdu+pq3e/IXr2GmtwLLwpzaa9PXy8EAysq559YT5ZijiL9LhB9rkRikUssc1IaYGFmgFdYz7TlhNN7By4vckuPkD44YJW1Mgewayup2RqdY5dnMZBIEC6l0uq55NPclwRRFk2302MMXiUrSwuiYtVVvQlZWsMxaeepMs65C1tS45o2vwPUyNXGU3ZKyQAM9SefTm5v5rrHKMLq7eV+T05csSHDG8LRMOqxrotAlLatTFjGNV9SjrDnNrQtPBXLld9qy+DhR545uL9osjrP/ezz6nIEf8kRvY1zV/h2NygqrLB2WRgxEI8CAwEAAaOBlDCBkTAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsGAQUFBwMBMEEGA1UdEQQ6MDiCE2F1dGguYW50aXBsYWdpYXQucnWGIWh0dHBzOi8vYXV0aC5hbnRpcGxhZ2lhdC5ydS9TYW1sMjAdBgNVHQ4EFgQUoUjMtHkHRjs21xBoerQXDCkJFzowDQYJKoZIhvcNAQEFBQADggEBAApOlmrBlnqLdQ+FPdhIZfQ7YBHyKqFZ8v8zlrNtZBOcq1v2P+28q//5iZcmyjnRg/qDHSjVmGV63x8d4Z1aanUriCFQ3BgDVA0uFKOzVAmVjnDWEgz5C3a3Y2+sNkaNTJwWl3Rcpv+A1E2Uj18jr66cEVwvxEnWSKJtgdBj4ZVN5nv5HbfPmvpKvxxQaj40pPe75Yj/r0f42JOFiY4QtT0m+/Z4OpjTaFrQ+1jc0XIoH/UcLRE2B+vPGdewvRjEw5WjssAhtZoxNKWe95WibanGh+Nceea3lTueARgSfA83aqymvaP1Dj8gJHkZezLQ9VlE1Xt4eYLgCYXGTSmjS6o=
                      </ds:X509Certificate>
                    </ds:X509Data>
                  </ds:KeyInfo>
                </KeyDescriptor>
                <NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:transient</NameIDFormat>
                <NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:persistent</NameIDFormat>
                <AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://auth.antiplagiat.ru/Saml2/Acs" index="0" isDefault="true"/>
                <AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Artifact" Location="https://auth.antiplagiat.ru/Saml2/Acs" index="1"/>
                <AttributeConsumingService index="0" isDefault="true">
                  <ServiceName xml:lang="en">Antiplagiat</ServiceName>
                  <ServiceName xml:lang="ru">Антиплагиат</ServiceName>
                  <ServiceDescription xml:lang="en">Antiplagiat.</ServiceDescription>
                  <ServiceDescription xml:lang="ru">Антиплагиат.</ServiceDescription>
                  <RequestedAttribute FriendlyName="eduPersonTargetedID" Name="urn:oid:1.3.6.1.4.1.5923.1.1.1.10" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri" isRequired="true"/>
                  <RequestedAttribute FriendlyName="eduPersonPrincipalName" Name="urn:oid:1.3.6.1.4.1.5923.1.1.1.6" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri" isRequired="true"/>
                  <RequestedAttribute FriendlyName="givenName" Name="urn:oid:2.5.4.42" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri" isRequired="true"/>
                  <RequestedAttribute FriendlyName="surname" Name="urn:oid:2.5.4.4" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri" isRequired="true"/>
                  <RequestedAttribute FriendlyName="apRole" Name="urn:oid:1.3.6.1.4.1.53915.1" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri" isRequired="true"/>
                  <RequestedAttribute FriendlyName="mail" Name="urn:oid:0.9.2342.19200300.100.1.3" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri" isRequired="false"/>
                  <RequestedAttribute FriendlyName="apStructureUnit" Name="urn:oid:1.3.6.1.4.1.53915.2" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri" isRequired="false"/>
                  <RequestedAttribute FriendlyName="apManagedStructureUnit" Name="urn:oid:1.3.6.1.4.1.53915.3" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri" isRequired="false"/>
                </AttributeConsumingService>
              </SPSSODescriptor>
              <Organization>
                <OrganizationName xml:lang="en">antiplagiat.ru</OrganizationName>
                <OrganizationDisplayName xml:lang="en">Antiplagiat</OrganizationDisplayName>
                <OrganizationDisplayName xml:lang="ru">Антиплагиат</OrganizationDisplayName>
                <OrganizationURL xml:lang="en">http://www.antiplagiat.ru/</OrganizationURL>
              </Organization>
              <ContactPerson contactType="support">
                <GivenName>Support</GivenName>
                <SurName>Team</SurName>
                <EmailAddress>mailto:support@antiplagiat.ru</EmailAddress>
              </ContactPerson>
            </EntityDescriptor>
          </EntitiesDescriptor>
        '''
        # based in SAMLMetadataResourceParser.parse()
        validation_errors = {}
        parse_saml_metadata(
            unicode_stream(xml),
            key=None,
            base_url='http://www.fedurus.ru/metadata/metadata.fedurus.xml',
            cleanup=[],
            fail_on_error=True,
            filter_invalid=True,
            validate=False,
            validation_errors=validation_errors,
        )
        # TODO: continue with the asserts when the previous call stop raising errors
