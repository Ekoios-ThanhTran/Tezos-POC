compile-all:
	bash ./scripts/compile.sh

deploy-all:
	make deploy-fungible deploy-nft deploy-singleAsset

deploy-fungible:
	./scripts/deploy.sh fungible

deploy-nft:
	./scripts/deploy.sh nft

deploy-singleAsset:
	./scripts/deploy.sh singleAsset
