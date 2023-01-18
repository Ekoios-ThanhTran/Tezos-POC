const { InMemorySigner } = require('@taquito/signer');
const { char2Bytes } = require('@taquito/utils');

const { TezosToolkit } = require('@taquito/taquito');
const { Tzip16Module } = require('@taquito/tzip16');
const { tzip16 } = require('@taquito/tzip16');

const { env } = require('../config');

const { rpc, account1, fungible } = env;

console.log(env);

async function offChainView() {
    const Tezos = new TezosToolkit(rpc);
    Tezos.addExtension(new Tzip16Module());

    const contract = await Tezos.contract.at(fungible, tzip16);

    // const metadata = await contract.tzip16().getMetadata();

    // console.log(metadata);

    const metadataViews = await contract.tzip16().metadataViews();

    // const TokenList = await metadataViews.all_tokens().executeView();

    // const tokenCount = await metadataViews.count_tokens().executeView();

    // const balance = await metadataViews.get_balance().executeView("tz1VZqbrSBTiVcETFTzJj6fqbzEBSsuvHf5Y", 0);

    // const tokenExisted = await metadataViews.does_token_exist().executeView(0);

    // const supply = await metadataViews.total_supply().executeView(0);

    console.log(metadataViews)
    // console.log(TokenList.reduce((pre, cur) => [...pre, cur.toString()], []))

    // console.log(tokenCount.toString())

    // console.log(balance.toString())
    // console.log(tokenExisted)
    // console.log(supply.toString())
}

function create_msg(arr) {
    return arr.reduce((pre, cur) => `${pre}0501${("00000000" + cur.length.toString(16)).slice(-8)}${char2Bytes(cur)}`, "")
}

async function signMsg() {
    const signer = await InMemorySigner.fromSecretKey("edskRuQFupsPcyYgvGEtLwNsDn8xVDrdLjKUL7C4fnWwd8GfVuoqSudvqyq2BSQkovfNPZjUoPSia6Wtsoa5JmbZNyxqZBGAMk");
    const newValue = "a".repeat(1000);
    const formattedInput = [
        '3sjdhfkhsdkfkasehfsdaksjdioejdsldjoiajsdiojsaoidjasjdjhasldljasdlj1231293877',
        newValue,
        '4'
    ];

    // The bytes to sign
    // const bytes = char2Bytes(formattedInput) + Number(69).toString(16);

    const bytes = create_msg(formattedInput);


    // console.log(bytes);

    // const bytes = STRING_OF_BYTES;
    const signature = await signer.sign(bytes);

    console.log(signature)
    return {
        signature,
        newValue,
    };
}

async function callContract() {
    const Tezos = new TezosToolkit(rpc);
    Tezos.setProvider({ signer: await InMemorySigner.fromSecretKey(account1.pk) });

    const contract = await Tezos.contract.at(fungible);

    console.log(contract.methods);

    

    // const op = await contract.methods.mint(
    //     "tz1VZqbrSBTiVcETFTzJj6fqbzEBSsuvHf5Y",
    //     100,
    //     {
    //         "token_id": char2Bytes("1"),
    //         "token_info": char2Bytes("aaa")
    //     },
    //     0
    // ).send();

    // const hash = await op.confirmation(3);
    // console.log(op.hash);
    // console.log(hash);
}

async function main() {
    // await signMsg();

    await offChainView();

    // await callContract();
}

main()
    .then(() => { })
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
