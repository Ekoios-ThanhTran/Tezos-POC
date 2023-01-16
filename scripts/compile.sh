
~/smartpy-cli/SmartPy.sh compile python/contracts/fungible.py output/contracts/fungible --html --purge
cp output/contracts/fungible/Fungible/step_000_cont_0_metadata.metadata_base.json metadata/fungible.json

~/smartpy-cli/SmartPy.sh compile python/contracts/nft.py output/contracts/nft --html --purge
cp output/contracts/nft/Nft/step_000_cont_0_metadata.metadata_base.json metadata/nft.json

~/smartpy-cli/SmartPy.sh compile python/contracts/singleAsset.py output/contracts/singleAsset --html --purge
cp output/contracts/singleAsset/SingleAsset/step_000_cont_0_metadata.metadata_base.json metadata/singleAsset.json
