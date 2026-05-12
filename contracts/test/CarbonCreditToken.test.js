const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("CarbonCreditToken", function () {
  let token, owner, addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    const CarbonCreditToken = await ethers.getContractFactory("CarbonCreditToken");
    token = await CarbonCreditToken.deploy();
    await token.deployed();
  });

  it("Should have correct name and symbol", async function () {
    expect(await token.name()).to.equal("AgriChain Carbon Credit");
    expect(await token.symbol()).to.equal("ACCC");
  });

  it("Should mint tokens", async function () {
    await token.mint(addr1.address, 1000, ethers.utils.formatBytes32String("farm1"));
    expect(await token.balanceOf(addr1.address)).to.equal(1000);
  });

  it("Should allow burning (retirement)", async function () {
    await token.mint(addr1.address, 1000, ethers.utils.formatBytes32String("farm1"));
    await token.connect(addr1).retire(500, ethers.utils.formatBytes32String("offset"));
    expect(await token.balanceOf(addr1.address)).to.equal(500);
  });

  it("Should enforce minter role", async function () {
    await expect(
      token.connect(addr1).mint(addr1.address, 100, ethers.utils.formatBytes32String("farm"))
    ).to.be.revertedWith("AccessControl");
  });
});

describe("CarbonCertificateNFT", function () {
  let nft, owner, addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    const NFT = await ethers.getContractFactory("CarbonCertificateNFT");
    nft = await NFT.deploy();
    await nft.deployed();
  });

  it("Should mint certificate", async function () {
    const tx = await nft.mintCertificate(
      addr1.address,
      ethers.utils.formatBytes32String("farm1"),
      100,
      "AC-CARBON-v1.0",
      "ipfs://metadata/1"
    );
    const receipt = await tx.wait();
    const tokenId = 1;
    const cert = await nft.getCertificate(tokenId);
    expect(cert.carbonTonnes).to.equal(100);
    expect(cert.owner).to.equal(addr1.address);
  });

  it("Should verify certificate", async function () {
    await nft.mintCertificate(
      addr1.address,
      ethers.utils.formatBytes32String("farm1"),
      100,
      "AC-CARBON-v1.0",
      "ipfs://metadata/1"
    );
    await nft.verifyCertificate(1);
    const cert = await nft.getCertificate(1);
    expect(cert.verified).to.equal(true);
  });
});

describe("FarmRegistry", function () {
  let registry, owner, addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    const Registry = await ethers.getContractFactory("FarmRegistry");
    registry = await Registry.deploy();
    await registry.deployed();
  });

  it("Should register farm", async function () {
    const farmId = ethers.utils.formatBytes32String("farm1");
    await registry.connect(addr1).registerFarm(farmId, "ipfs://farm1", 5, "maize", "Kenya");
    const farm = await registry.getFarm(farmId);
    expect(farm.areaHectares).to.equal(5);
    expect(farm.farmer).to.equal(addr1.address);
  });

  it("Should verify farm", async function () {
    const farmId = ethers.utils.formatBytes32String("farm2");
    await registry.connect(addr1).registerFarm(farmId, "ipfs://farm2", 10, "coffee", "Rwanda");
    await registry.verifyFarm(farmId);
    const farm = await registry.getFarm(farmId);
    expect(farm.verified).to.equal(true);
  });
});
