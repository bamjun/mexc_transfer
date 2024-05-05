use etherscan;


CREATE TABLE address (
    id INT PRIMARY KEY AUTO_INCREMENT,
    address VARCHAR(42) NOT NULL UNIQUE, 
    balance DECIMAL(30,18) DEFAULT 0,
    INDEX (address) -- 인덱스 추가
);


SELECT * FROM etherscan.address;

SELECT count(*) FROM etherscan.address2 where balance > 0 and balance < 2 order by balance desc;
SELECT * FROM etherscan.address2 where balance > 0 and balance < 2 order by balance desc;
SELECT count(*) FROM etherscan.address2 where balance > 0;
SELECT * FROM etherscan.address2 order by id desc;
SELECT count(*) FROM etherscan.address2;


SELECT count(id) FROM etherscan.address;

select * from etherscan.address where address = '0x6593c7de001fc8542bb1703532ee1e5aa0d458fd';