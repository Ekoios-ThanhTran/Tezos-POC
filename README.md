



## Execute the tests

```bash
~/smartpy-cli/SmartPy.sh test python/tests/collaborationContract_test.py output/tests/collaborationContract --html --purge
```

## Compile the contracts

```bash
~/smartpy-cli/SmartPy.sh compile python/contracts/checkSignature.py output/contracts/checkSignature --html --purge

~/smartpy-cli/SmartPy.sh compile python/contracts/stringUtils.py output/contracts/stringUtils --html --purge

~/smartpy-cli/SmartPy.sh compile python/contracts/nft.py output/contracts/nft --html --purge


```