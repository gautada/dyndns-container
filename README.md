# dynip

## Adstract

[DynIP](https://github.com/gautada/dynip-container) is a dynamic ip tool that determines the external IP address and updates a dns 
servics. This container serves a microservice as an API for other services. 

## Features

- Microservice - [API](https://fastapi.tiangolo.com) server.
- Plugin Architecture - A simple mechanism to support multiple dns providers
 - Hover Plugin - Access client for the Hover API
- Client - A cli client for use with crond to invoke the lookup/update

### Feature Detail

#### Microservice

- **/ip** Lookup the external IP.  Returns previous and current ip, as well as the last timestamp inside a status envelope.
- **/host** Update the IP for an fqdn.  This method takes plugin, name(host), and domain to form the fqdn for a specific service. There are two method `get` retrieve the dns record; the `post` updates the dns record with an additional param for ip.
- **/field** Update the content for TXT record. This is the same parameters as `/host`.

#### Plugin Architecture

This provides a mechanism for connecting to DNS providers in a standard way. The interface is defined in the `dyndns_plugin.py` file.  

**Providers**

- Hover: Uses the api provided by hover.  It is fairly simple and I will let the code speak for itself.

#### Client

The `client.py` provides a simple script to use the API.  This should be referenced for any other clients using the API.  For consistency the **client** uses the same config file `/etc/container/dyndns.yml`.
 

## Development

### Configuration

To configure the service a config file `/etc/container/dyndns.yml` must be provided.  Below is an example only the `hover` plugin is working.

```
plugins:
  - name: hover
    username: {USERNAME}
    password: {PASSWORD}
    domains:
      {DOMAIN}.{TLD}:
      - {HOST1}
      - {HOST2}
      - {HOST3}
  - name: route53
    user: example
    password: actualpwd
    domains:
      foobar.org
      - xyz
      - abc

```

## Architecture

### Context

![Context Diagram](https://plantuml.com/plantuml/svg/fLDjRzem4FxEhxX5anOa86sXxLfjHIkm5gbZRBJQXsf29Zc8LSUER0U8WF--Su3IbxMQkYYAp-UxvxaxFtd7PIYo2E5Jgn6q6hKqIyHPwTrZxx2bfCMvVUMKSOdwnVCaLHBbI_djNBA4Xo-TOYfKdkpIInzWCSYDnMJPeR9qghd1uUfSPJ9YElUPuCnKGB0HYWeicZPFSLM1fcKJShyNNDwL2QEFsYYv67RcTlKafncX2JMjXh0jFikbxCr4oAgk7xBMHRq5SGDO3747MO3U-nVjqRB5mXYNVoMm6CRo7qlVNCSpfet__vYQEwQVA9ZbIfgOfm_9rdoBSxwYY4LNHZZtkVik_R5M2LsMLM_XwocBPaj4gwGzUDSnDq0lA_OUC0DodqvT7X51s00Kc9oI5ywWQBP0ksqre2-Oj3VVhdxxiRMfEGs2r7b8XrLZ8y57jGctSJQgSKLQhMx30oUmsmjkB5nZGYaMTmWJSc_JGfK44vPP5h5WVyIEFXwo-idXyV6upev2ThA71_LHus2ylrVVPmLcPyu83ys3WZAj9veb2PUJck1Z348JX8tgjj3owvWbowsWAMq43MtE71fKWNxBTc-m4w1NAgqLxdjHBYDfl0fuww2DvVvYS3bL6A0jh6uVHinW14f2I9MIl63AH8PUUOFcDEPxFENZtC5q-sJ0btxNRMW1WthAGtGt9PIwgsOfs1Y1QaKjcN0CB8eq6bTF8VFFtdOsBEMr0hcczEG9Owocr1EHN3uoNEDKzvOrrMhA8tBxOwKJ9aGErrcePgRyd6qsczKAL7Ujn5OYTJ-SrNsFLzG7jU5t-sKAUn9rNzTD6f5kmF_wezqxNOUM1fVVVmslEXUTNjil_m40)


## Administration

### Issues

The official to list is kept in a [GitHub Issue List](https://github.com/gautada/dynip-container/issues/)

## Notes

- Updated to the latest spec [Issue #4](https://github.com/gautada/dyndns-container/issues/4)
