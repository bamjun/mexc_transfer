use etherscan;


CREATE TABLE address (
    id INT PRIMARY KEY AUTO_INCREMENT,
    address VARCHAR(42) NOT NULL UNIQUE, 
    balance DECIMAL(30,18) DEFAULT 0,
    INDEX (address) -- 인덱스 추가
);