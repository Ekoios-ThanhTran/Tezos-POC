#!/bin/bash

export RPC=https://ghostnet.ecadinfra.com/
export PK=edskRuQFupsPcyYgvGEtLwNsDn8xVDrdLjKUL7C4fnWwd8GfVuoqSudvqyq2BSQkovfNPZjUoPSia6Wtsoa5JmbZNyxqZBGAMk

function fungible {
    echo "deploying fungible contract..."
    ~/smartpy-cli/SmartPy.sh originate-contract --code output/contracts/fungible/Fungible/step_000_cont_0_contract.tz --storage output/contracts/fungible/Fungible/step_000_cont_0_storage.tz --rpc $RPC --private-key $PK
}

function nft {
    echo "deploying nft contract..."
    ~/smartpy-cli/SmartPy.sh originate-contract --code output/contracts/nft/Nft/step_000_cont_0_contract.tz --storage output/contracts/nft/Nft/step_000_cont_0_storage.tz --rpc $RPC --private-key $PK
}

function singleAsset {
    echo "deploying singleAsset contract..."
    ~/smartpy-cli/SmartPy.sh originate-contract --code output/contracts/singleAsset/SingleAsset/step_000_cont_0_contract.tz --storage output/contracts/singleAsset/SingleAsset/step_000_cont_0_storage.tz --rpc $RPC --private-key $PK
}

subcommand="$1"
shift

case $subcommand in
    fungible)
        fungible
        ;;
    nft)
        nft
        ;;
    singleAsset)
        singleAsset
        ;;
    *)
        echo "unknown command '$subcommand'"
        ;;
esac
