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
- **/record** Update the IP for an fqdn.  This method takes plugin, name(host), and domain to form the fqdn for a specific service. There are two method `get` retrieve the dns record; the `post` updates the dns record with an additional param for ip.
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

![Context Diagram](https://www.plantuml.com/plantuml/svg/fLJlRjis4F-kf-2C0PE1M6eQjrsBhMbh6wc1B3Fg5Fam3C6PEbj4AP8WJqaC9---erHDdPDqHMiOrl78tn_T7Vqc47YgAvtyf8pKTO7YjyaudumpnydN-zdBYJM4D_ILNL06_QFxbRC6pMFuwTP0fUHZk-YqtLOzFFb5x9RRG5ZTpjYMTru5lBnxPsjJWD-ce1M40w5XXVf0x8vfw_3kG1mJR3ZzirRcqv0v5kY3DRlBsGtTxM6E2mpIypCmD-4zBAC_LuIZKVlXg3NrFOoHi2jYJnb9-_nkkhgTW2pnza41GbcQRxFUjMDVgSl_cD9nh_G1DP2o9fJAzMATtkwTkkCJkxafy2PLyVSsNNjRSRF8Ve_UcIKC_EmK3A_5uBnKGV0NclL0G13ca7SZZeM470lKMBtYh7WjcfTjsFwQZCL2Ww6FVvp-dPP4BhpASnSpF8UZG8LMgsoZgAnNcR8ygwFkU3wC-1CLI9nZnH32dc73wGucRPLle2Oe83zSmVDVdy7HosSlNgoFuBc4bq_mwT5g_7Hz-EJe41hEsGqm7uOl3DNURpnKbJARJAirvZBaSZpgZ0w_pfcG8irL-ZpGOgeWiecHu6ivFLls0pX8agIzDEa0wi290p5uMrE9XfG4ma9yZDbXqbw4E3pfG6h5-_7ef8d4KdhbgC4AsQPa9o6e11BC7JX2yNOn_vSj7HHRKvWGWQspDch-EWGlsV4IgOdc2x62m7wi4PBB4pMkGDUuvqqvjTv6clc2WqQE5_mG0VsLaXZ7GrlxQLIxnX0N2Bq17HMWA3m6zjFUhTy7NKF0gQnXpgpVx2cMzggjs_l_16BK-EvKdRTNgk1qkhQ-0gstuhoMzZeCxwjTNrzd3MkS9LPB-4hr_VcYQ1Uu4dF3_jSWaHCj0oCOqBUfGtI568aJfFZkNI4Vh477bcwGXcmgox9SkM_ZXkRLFKhhYmU9sgt_9ri-IkPiU9Yjv-XduPJxNRjx1_hMVK0eyWkl26Evb-__lBWydPtCpgRfC7c3fgWh_Gy0)

### Container

![Containter Diagram](https://www.plantuml.com/plantuml/svg/fLLjRzis4FwkNt4r1am6Ohjft5Ti3HexQmEqgT4as8TY26ZgP16XI86aaXYE__kEb2mfTbmCcM7OvF5U7jxBmnT2SLac27zCngF9U5YKkVmOlNWilPvevV3U_UAK2OLcxtbUQ8Lgd_rqgLWk-BvJBAHUvgrvz3kiBfRMOVvmIh1COOJ5w_M9BbN2p39cKZ1x09BDKHx0wjWj2rmVmB5Z2nB_9eMwwPEF6HghrUhwzDwjjsoE4xJSqBybtmvtRCcwpWYj1jM7LXMevtYi7OOajYw3qqQ-ciuV9end-F1a08SyK_yHUbsEdKYr_Fz5EcuZ_K39dD3APgBe1glYhKx4cZHMPoh1-rZutuSuDJgdOZdzd7Zdsg7T1A9_HNleNMR20drPsFU0ML27TEhjA13mCQ34_0D9uIE4omPlFoTZc4cctDMth__4cNE5_J0Q5Lv2VJYmBf5YFbm8bvNpeT3KguED-iWtsC_FmZgun9nC7BOU5YJUc76TZnQiT2nXeyCvU_FkDJjw__hjs_I8lU7i_KjyTJGVlqeFNnuTik3pz9wHFxGTGAKn2yFoNAZ5K8eKHzoE-7Ym0Th_jS_82ISfIqsVmLGmxmy6G8CvFRzeMx0NHL4rDhunuXuhBGaFeFUfT1arZk1qqGIklBGVDMQLCfU2LBpsf5fHx6PcUxo9ST31uZVjIHzMKGicxXL6Eysrz5gpUWqNQ6vhKBCps1A7fCMsJx6xZbXHI8-TMZKORcs174ZaVWywXMBfCbfHCuh2MN0PSv2p6mJA1kqGqb85PIQXunbIRI1PgaJPeRyxj9UtD6j9AIlO5yqctBUBiomIIh1NkcfMLJ9hD1KOmc4349y1Ql3AB4Y8ij1uO5ETarEQKD-DPWcnGQvDOljX8gYblDEpcK_KkWjrplXDMGnyKOpFIe1y4eG1AGcVGbwPTNJ_gdCKRkoOzvv0fTNa3tAaJ2Sx62XuAXPrez2gD5MjTgBoHySx-jtGZrIfd8ejCBmvEz4B6W3A6IeUyZ_hR2i06zP1Wvvsb8QE2IZ4X6R4DuFpn4IpSYiuqLdAXDJKezuc8rGqbCHKL1Q3LBrXu2sg8xls_hSmvLe9fqCjljNBBfPQHWG1iTGBoDlzhM2GIirl-XLMjoc-N8BmJEEJG7YfLm9SLBV2Q5MbnaEgVJs5IYXghJAlf_witNMnjM8BSMiHwl1SJAsR1jOwYghdkI8ZKOXq6L3DQE47PSCOTJty64YjRmRKZuy6vsm6B4aCMjkhNzK_UnigPeKO1iz3RHRKEDs8cQvfwSkZXMTPejXDLAAqMv6GEAO6oPca6r-MNDyHPUr4kxkx6mQl_XNnZ4AFQOUJk-puAQ7NmNUWiQGOz5ewxYeITJSQNVaMGmOsRHIt3dUcxWUcdS0jYUqBt9B5ZgkAFVO4ReeweSJjGzVKOQCKNNpv_lVrrzFFf-VJkFyl)

### Component

![Component Diagram]()



## Administration

### Issues

The official to list is kept in a [GitHub Issue List](https://github.com/gautada/dynip-container/issues/)

## Notes

- Updated to the latest spec [Issue #4](https://github.com/gautada/dyndns-container/issues/4)
