INSERT INTO user (username, password, email, phone, first_name, middle_name, last_name, address, occupation)
VALUES
    ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'abc@gmail.com', '123-145-147', 'Hello', 'T.', 'Wang', '555 Westwood Plaza level, Los Angeles, CA 90095', 'Professor'),
    ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', 'cdf@yahoo.com', '456-789-963', 'Name', 'M.', 'Last', '10980 Wellworth Ave, Los Angeles, CA 90024', 'CEO');