<?php
require_once 'conecxao/config.php';

// Verifica se veio do formulário
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // Pegando dados com segurança
    $cep = $_POST['cep'] ?? '';
    $numero = $_POST['numero'] ?? '';
    $telefone = $_POST['telefone'] ?? '';
    $email = $_POST['email'] ?? '';
    $senha = $_POST['senha'] ?? '';
    $nome = $_POST['nome'] ?? '';

    // Validação básica
    if (empty($nome) || empty($email) || empty($cep) || empty($numero)) {
        echo "Preencha todos os campos obrigatórios!";
        exit;
    }

    // Prepared Statement (SEGURANÇA)
    $stmt = $conn->prepare("INSERT INTO usuarios 
        (cep, numero, telefone, email, senha, nome) 
        VALUES (?, ?, ?, ?, ?, ?)");

    $stmt->bind_param("sssisi", $cep, $numero, $telefone, $email, $senha, $nome);

    if ($stmt->execute()) {
        echo "✅ Usuário criado com sucesso!";
    } else {
        echo "❌ Erro ao salvar: " . $stmt->error;
    }

    $stmt->close();
    $conn->close();

} else {
    echo "Acesso inválido!";
}
?>