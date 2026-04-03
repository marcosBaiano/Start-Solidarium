<?php
require_once 'conecxao/config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $nome = $_POST['nome'] ?? '';
    $email = $_POST['email'] ?? '';
    $cep = $_POST['cep'] ?? '';
    $numero = $_POST['numero'] ?? '';
    $tipo_endereco = $_POST['tipo_endereco'] ?? '';
    $quantidade = $_POST['quantidade'] ?? '';

    if (empty($nome) || empty($email) || empty($cep) || empty($numero)) {
        echo "Preencha todos os campos obrigatórios!";
        exit;
    }

    $stmt = $conn->prepare("INSERT INTO solicitacoes 
        (nome, email, cep, numero, tipo_endereco, quantidade) 
        VALUES (?, ?, ?, ?, ?, ?)");

    $stmt->bind_param("sssisi", $nome, $email, $cep, $numero, $tipo_endereco, $quantidade);

    if ($stmt->execute()) {
        echo "Solicitação enviada com sucesso!";
    } else {
        echo " Erro ao salvar: " . $stmt->error;
    }

    $stmt->close();
    $conn->close();

} else {
    echo "Acesso inválido!";
}
?>