<!-- Script SQL para criar o banco de dados e as tabelas para o aplicativo StartSolidarium.
 Este script deve ser executado em um ambiente de banco de dados MySQL para configurar a estrutura necessária para o aplicativo.
 Ele inclui a criação do banco de dados, bem como as tabelas para usuários, solicitações e coletas.
 Certifique-se de ajustar as credenciais de conexão e as configurações conforme necessário para o seu ambiente. -->

CREATE DATABASE startSolidarium;

USE startSolidarium;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cep VARCHAR(9) NOT NULL,
    numero INT NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE solicitacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cep VARCHAR(9) NOT NULL,
    numero INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL,
    tipo_endereco ENUM('empresa','condominio','particular') NOT NULL,
    quantidade INT NOT NULL,
    status ENUM('pendente','em_andamento','concluido') DEFAULT 'pendente',
    data_solicitacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE coletas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_solicitacao INT,
    data_coleta DATETIME,
    responsavel VARCHAR(100),
    status ENUM('agendada','coletado','cancelado') DEFAULT 'agendada',
    
    FOREIGN KEY (id_solicitacao) REFERENCES solicitacoes(id)
);