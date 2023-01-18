const { InMemorySigner } = require('@taquito/signer');
const { char2Bytes } = require('@taquito/utils');

const { TezosToolkit } = require('@taquito/taquito');
const { Tzip16Module } = require('@taquito/tzip16');
const { tzip16 } = require('@taquito/tzip16');

const { TezosMessageUtils } = require('conseiljs');

const { env } = require('../config');

const { rpc, account1, account2, account3, singleAsset } = env;

// console.log(env);

async function offChainView() {
    const Tezos = new TezosToolkit(rpc);
    Tezos.addExtension(new Tzip16Module());

    const contract = await Tezos.contract.at(singleAsset, tzip16);

    // const metadata = await contract.tzip16().getMetadata();

    // console.log(metadata);

    const metadataViews = await contract.tzip16().metadataViews();

    const TokenList = await metadataViews.all_tokens().executeView();

    const balance1 = await metadataViews.get_balance().executeView(account1.address, 0);
    const balance2 = await metadataViews.get_balance().executeView(account2.address, 0);
    const balance3 = await metadataViews.get_balance().executeView(account3.address, 0);


    const supply = await metadataViews.total_supply().executeView(0);

    console.log(metadataViews)

    console.log("token list: " + TokenList.reduce((pre, cur) => [...pre, cur.toString()], []));
    console.log("account1 balance: " + balance1.toString());
    console.log("account2 balance: " + balance2.toString());
    console.log("account3 balance: " + balance3.toString());
    console.log("total supply: " + supply.toString());
}

function create_msg(arr) {
    return arr.reduce((pre, cur) => `${pre}0501${("00000000" + cur.length.toString(16)).slice(-8)}${char2Bytes(cur)}`, "")
}

async function signMintMsg({ to_, amount }) {
    const signer = await InMemorySigner.fromSecretKey(account1.pk);
    const formattedInput = [
        amount.toString(),
    ];

    // The bytes to sign
    // const bytes = char2Bytes(formattedInput) + Number(69).toString(16);

    const bytes = TezosMessageUtils.writeAddress(to_) + create_msg(formattedInput);


    // console.log(bytes);

    // const bytes = STRING_OF_BYTES;
    const signature = await signer.sign(bytes);

    // console.log(signature)
    return signature;
}

async function callContract() {
    const Tezos = new TezosToolkit(rpc);
    Tezos.setProvider({ signer: await InMemorySigner.fromSecretKey(account1.pk) });

    const contract = await Tezos.contract.at(singleAsset);

    console.log(contract.methods);

    await offChainView();

    console.log("=>>> mint [100, 100] tokens to [account1, account2]...")
    const opMint = await contract.methods.mint([
        {
            to_: account1.address,
            amount: 100,
        },
        {
            to_: account2.address,
            amount: 100,
        }
    ]).send();
    await opMint.confirmation();
    console.log("TX hash: " + opMint.hash);
    await offChainView();

    console.log("=>>> Transfer 100 token from account1 to account2...")
    const opTransfer = await contract.methods.transfer([
        {
            from_: account1.address,
            txs: [
                {
                    to_: account2.address,
                    token_id: 0,
                    amount: 100,
                },
            ]
        },
    ]).send();
    await opTransfer.confirmation();
    console.log("TX hash: " + opTransfer.hash);
    await offChainView();

    await approve();

    console.log("=>>> account1 transfer 100 token from account2 to account3...")
    const opTransfer1 = await contract.methods.transfer([
        {
            from_: account2.address,
            txs: [
                {
                    to_: account3.address,
                    token_id: 0,
                    amount: 100,
                },
            ]
        },
    ]).send();
    await opTransfer1.confirmation();
    console.log("TX hash: " + opTransfer1.hash);
    await offChainView();

    await mintSignature();
    await offChainView();

    // const hex = TezosMessageUtils.writeAddress(account2.address);
    // console.log(hex);
    // const hash = await op.confirmation(3);
    // console.log(hash);
}

async function approve() {
    const Tezos = new TezosToolkit(rpc);
    Tezos.setProvider({ signer: await InMemorySigner.fromSecretKey(account2.pk) });
    const contract = await Tezos.contract.at(singleAsset);

    console.log("=>>> approve account1 to transfer token from account2...")
    const opApprove = await contract.methods.update_operators([
        {
            add_operator: {
                owner: account2.address,
                operator: account1.address,
                token_id: 0
            }
        },
    ]).send();
    await opApprove.confirmation();
    console.log("TX hash: " + opApprove.hash);
}

async function mintSignature() {
    const Tezos = new TezosToolkit(rpc);
    Tezos.setProvider({ signer: await InMemorySigner.fromSecretKey(account2.pk) });
    const contract = await Tezos.contract.at(singleAsset);

    const sig = await signMintMsg({
        to_: account2.address,
        amount: "100",
    });
    console.log(sig);
    // 0000ea8c13ff02adc10b24b258474f4f8ac362789ce8
    // 050a000000160000ea8c13ff02adc10b24b258474f4f8ac362789ce8050100000003313030
    // 050100000024747a31683243636f657a664870467053397650626851796b33786375366f505956566b6d050100000003313030

    console.log("=>>> mint 100 tokens to account2 with admin signature...")
    const opMint = await contract.methods.mint_signature([
        {
            to_: account2.address,
            amount: 100,
            signature: sig.prefixSig
        },
    ]).send();
    await opMint.confirmation();
    console.log("TX hash: " + opMint.hash);
}

async function main() {

    await callContract();
}

main()
    .then(() => { })
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
