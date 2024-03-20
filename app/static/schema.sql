CREATE TABLE email_creds (
	email VARCHAR(500) NOT NULL COMMENT 'Primary Key',
	domain VARCHAR(100) NOT NULL,
	email_pass VARCHAR(500) NOT NULL,
	email_host VARCHAR(300) NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	created_by VARCHAR(200) NOT NULL,
	PRIMARY KEY (email)
);

ALTER TABLE email_creds
ADD COLUMN port INT NOT NULL;

CREATE TABLE wireless_carrier_email_text (
	id INT NOT NULL AUTO_INCREMENT,
	wireless_carrier VARCHAR(200) NOT NULL,
	domain VARCHAR(200) NOT NULL,
	allow_multimedia BOOLEAN NOT NULL,
	created_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	UNIQUE KEY unique_carrier (wireless_carrier,domain,allow_multimedia) USING BTREE,
	PRIMARY KEY (id)
);