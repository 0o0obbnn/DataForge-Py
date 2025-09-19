-- DataForge 导出数据
-- 导出时间: 2025-09-15 09:48:54

CREATE TABLE IF NOT EXISTS generated_data (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  age INT,
  email VARCHAR(200),
  phone VARCHAR(50)
);

INSERT INTO generated_data (name, age, email, phone) VALUES
('周磊', 20, '5u7k7sock1@ojlajo.net', '15 36611 2148'),
('刘丽', 45, '1oocpp9@ewixatoh.cn', '19 93154 2932'),
('王涛', 27, 'eom3rq@azua.cn', '15 44120 5689'),
('陈磊', 32, 'oltugp_a@icqmrad.org', '15 76428 8845'),
('吴婷', 56, 'd9fr_c@oct.emrhf.org', '18 62223 1439');
