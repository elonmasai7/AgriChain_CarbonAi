const hre = require("hardhat");

async function main() {
  console.log("Deploying AgriChain Carbon AI Contracts...\n");

  const [deployer] = await hre.ethers.getSigners();
  console.log(`Deploying with account: ${deployer.address}\n`);

  const CarbonCreditToken = await hre.ethers.getContractFactory("CarbonCreditToken");
  const token = await CarbonCreditToken.deploy();
  await token.deployed();
  console.log(`CarbonCreditToken deployed: ${token.address}`);

  const CarbonCertificateNFT = await hre.ethers.getContractFactory("CarbonCertificateNFT");
  const nft = await CarbonCertificateNFT.deploy();
  await nft.deployed();
  console.log(`CarbonCertificateNFT deployed: ${nft.address}`);

  const FarmRegistry = await hre.ethers.getContractFactory("FarmRegistry");
  const registry = await FarmRegistry.deploy();
  await registry.deployed();
  console.log(`FarmRegistry deployed: ${registry.address}`);

  const CarbonMarketplace = await hre.ethers.getContractFactory("CarbonMarketplace");
  const marketplace = await CarbonMarketplace.deploy(nft.address, token.address);
  await marketplace.deployed();
  console.log(`CarbonMarketplace deployed: ${marketplace.address}`);

  const MultiSigVerification = await hre.ethers.getContractFactory("MultiSigVerification");
  const multisig = await MultiSigVerification.deploy();
  await multisig.deployed();
  console.log(`MultiSigVerification deployed: ${multisig.address}\n`);

  await token.grantRole(await token.MINTER_ROLE(), nft.address);
  console.log("Granted MINTER_ROLE to CarbonCertificateNFT");

  console.log("\nDeployment complete!");
  console.log("====================");
  console.log(`CarbonCreditToken:     ${token.address}`);
  console.log(`CarbonCertificateNFT:  ${nft.address}`);
  console.log(`FarmRegistry:          ${registry.address}`);
  console.log(`CarbonMarketplace:     ${marketplace.address}`);
  console.log(`MultiSigVerification:  ${multisig.address}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
