# Default mnemonic length of legacy-by-default wallets, May 2020

**Population.** Every single-signature wallet whose *only* Bitcoin path in the walletsrecovery.org snapshot is legacy: BIP44 `m/44'…`, or BRD-style `m/0'`.
- Snapshot: [nvk/walletsrecovery.org @ 80436a2b98, 2020-05-29](https://github.com/nvk/walletsrecovery.org/blob/80436a2b98/README.md).
- The snapshot lists supported paths only, not defaults and not mnemonic lengths. A wallet with one legacy path is legacy by construction; multi-path wallets are excluded because their default can't be read from the snapshot.
- Also excluded: wallets with no mnemonic (Bitcoin Core, the Bitcoin Wallet app, Opendime), multisig wallets (BTC.com, Unchained, Green), and DropBit (new wallets default to `m/84`).

**Length evidence.** Taken from each wallet's source code at its last commit on or before 2020-05-10 **[SOURCE]**, or else from vendor documentation **[DOC]**, which is undated and not measured.

| wallet | default length | evidence |
|---|---|---|
| Blockchain.com | **12** [SOURCE] | [`BIP39.generateMnemonic(undefined, …)`](https://github.com/blockchain/my-wallet-v3/blob/c0bf5615c8/src/blockchain-wallet.js#L731); its pinned bip39 2.1.x has [`strength = strength \|\| 128`](https://github.com/bitcoinjs/bip39/blob/2.1.2/index.js#L75) |
| BRD | **12** [SOURCE] | [`UInt128 entropy` → `BRBIP39Encode`](https://github.com/breadwallet/breadwallet-core/blob/73566cb79f/crypto/BRCryptoAccount.c#L56) |
| Hodl Wallet (BRD fork) | **12** [SOURCE] | [`BRBIP39Encode(…, MemoryLayout<UInt128>.size)`](https://github.com/hodlwallet/hodl-wallet-ios/blob/fbdf286daa/hodlwallet/src/WalletManager+Auth.swift#L364) |
| Copay | **12** [SOURCE] | [`new Mnemonic(wordsForLang[…])`](https://github.com/bitpay/bitcore/blob/2cc9361446/packages/bitcore-wallet-client/src/lib/key.ts#L70); [bitcore-mnemonic: `ent = ent \|\| 128`](https://github.com/bitpay/bitcore/blob/2cc9361446/packages/bitcore-mnemonic/lib/mnemonic.js) |
| Bisq | **12** [SOURCE] | bitcoinj fork: [`new DeterministicSeed(…, DEFAULT_SEED_ENTROPY_BITS, "")`](https://github.com/bisq-network/bitcoinj/blob/a3644e9243/core/src/main/java/org/bitcoinj/wallet/KeyChainGroup.java#L96), where [`DEFAULT_SEED_ENTROPY_BITS = 128`](https://github.com/bisq-network/bitcoinj/blob/a3644e9243/core/src/main/java/org/bitcoinj/wallet/DeterministicSeed.java#L46) |
| Coin Wallet | **12** [SOURCE] | [`rng(128 / 8)`](https://github.com/CoinSpace/CoinSpace/blob/da8416dccf/app/lib/wallet/index.js#L69) |
| OpenBazaar | **12** [SOURCE] | [`newEntropy(128)`](https://github.com/OpenBazaar/openbazaar-go/blob/755e0251bb/repo/init.go#L216) |
| Multibit HD (discontinued 2017) | **12** [SOURCE] | ["Default to twelve word seed" → `TWELVE_WORDS`](https://github.com/bitcoin-solutions/multibit-hd/blob/24a12b199a/mbhd-swing/src/main/java/org/multibit/hd/ui/views/components/display_seed_phrase/DisplaySeedPhraseModel.java#L38) |
| KeepKey (device) | **12** [SOURCE], applying when the host omits a strength | [`msg->has_strength ? msg->strength : 128`](https://github.com/keepkey/keepkey-firmware/blob/cc378f2007/lib/firmware/fsm_msg_common.h#L358) |
| KeepKey Client | **not determined** | `keepkey/keepkey-client` has no commit before May 2020; the host-side default is unread |
| Atomic Wallet | **12** [DOC] | [support.atomicwallet.io, article 35](https://support.atomicwallet.io/article/35-what-is-12-word-recovery-phrase) |
| Jaxx Liberty | **12** [DOC] | [Jaxx Liberty support, article 115000809413](https://support.decentral.ca/hc/en-us/articles/115000809413-How-can-I-get-my-12-word-Backup-Phrase-) |
| Luxstack | **not found** | — |

## Counts (13 wallets)

| default length | wallets |
|---|---|
| 12 | **11** (9 from source, 2 from docs) |
| 15 | 0 |
| 18 | 0 |
| 21 | **0** |
| 24 | **0** |
| not determined | 2 (KeepKey Client, Luxstack) |

For comparison, outside the snapshot: the iancoleman BIP39 tool as of 2020-05-08 defaults to the BIP44 tab (legacy) and to **15** words. It offers 21 and 24 as choices. [SOURCE: `src/index.html` @ 115eb45]
