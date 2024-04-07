# Cardano Watcher
#### A KERI watcher for Identifiers witnessed by Cardano blockchain and more.

This project was funded by [Project Catalyst](https://projectcatalyst.io), a decentralized innovation engine for solving real-world challenges based Cardano blockchain; it's tracked under [Idea #112426](https://projectcatalyst.io/funds/11/cardano-open-developers/gleif-network-super-watcher-on-cardano-by-rootsid-725aa).

## Motivation
The [KERI protocol](https://weboftrust.github.io/ietf-keri/draft-ssmith-keri.html) is a fully decentralized identity protocol for persistent self-certifying identifiers called Autonomic Identifiers (AIDs). The **primary root-of-trust** are the self-certifying identifiers that are strongly bound at issuance to a cryptographic signing (public, private) keypair that can be later rotated using an end-verifiable Key Event Log (KEL) mechanism.

The indirect mode of the protocol depends on witnessed key event receipt logs (KERL) as a **secondary root-of-trust** for validating events. Those receipts are produced by a set of **witnesses** assigned by the controller of the AID and the security and accountability guarantees are provided by KA2CE or KERI's Agreement Algorithm for Control Establishment.

A special case is when a blockchain is used to validate and anchor the key events to the ledger since the consensus mechanism of the ledger provides the accountability guarantees of the KEL. A Proof of Concept of a Cardano Witness was developed by [RootsID](https://www.rootsid.com) and can be found [here](https://github.com/weboftrust/cardano-backer). Furthermore, [Cardano Foundation](https://cardanofoundation.org) is developing a [wallet](https://github.com/cardano-foundation/cf-identity-wallet?tab=readme-ov-file) that use Cardano as a witness of key event from identifiers.

This project is about **watchers** that are entities that keep a copy of a KERL for an identifier but are not designated by the controller thereof as one of its witnesses. An identifier watcher is part of the trust basis of a validators that need protection against duplicity events and malicious activity. The **watcher** is an observer that acts as a Jury when divergence, inconsistent or suspicious activity is detected. Hence, the goal of the watcher is to detect dishonest identity controllers or malicious third party may have exploited vulnerabilities on the controller of the identifier.

In this case we are developing a **Cardano Watcher** that is primarily focused on "watching" Key Events Logs that were achored to the Cardano Blockchain but also the design considers event produced by non-blockchain witnesses and other functionalities needed by verifiers.

## Project resources
* [Catalyst Project](https://projectcatalyst.io/funds/11/cardano-open-developers/gleif-network-super-watcher-on-cardano-by-rootsid-725aa) proposal, funds allocated and distributed 
* Catalys Project [milestones].(https://milestones.projectcatalyst.io/projects/1100144) and Proofs of Achievement.
* [Design](DESIGN.md)
* [Project Plan](https://github.com/roots-id/cardano-watcher/milestones) and followup
* [License](LICENSE)
