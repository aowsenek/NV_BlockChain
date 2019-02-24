
pragma solidity ^0.5.0;

contract nv_hash_publisher {
    
    struct Block_Hashes {
        string hash;
        uint epoch;
        uint nonce;
    }
    address Neutral_Vehicle = 0xDa0825612e65398C524cf9f34BaE231C7cF48b2B;
    Block_Hashes[] public Block_Data;
    event NewBlock(string hash, uint epoch, uint nonce);

    
    function addHash(string memory hash, uint epoch, uint nonce) public {
       // Block_Hashes memory newblock = Block_Hashes(hash, epoch, nonce);
        Block_Data.push(Block_Hashes(hash, epoch, nonce));
        emit NewBlock(hash, epoch, nonce);
    }
    function getHash(uint blockNumber) public view returns(string memory, uint, uint) {
        Block_Hashes memory tempblock;
        tempblock = Block_Data[blockNumber];    
        return(tempblock.hash, tempblock.epoch, tempblock.nonce);
    }
}

