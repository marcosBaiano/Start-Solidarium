<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Start Solidarium - Solicitação</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            width: 400px;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
        }

        h2 {
            text-align: center;
            color: #2ecc71;
            margin-bottom: 20px;
        }

        input, select {
            width: 100%;
            padding: 10px;
            margin-bottom: 12px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }

        button {
            width: 100%;
            padding: 12px;
            background: #2ecc71;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }

        button:hover {
            background: #27ae60;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>Solicitar Coleta</h2>

    <form action="back/criarSolicitacao.php" method="POST">    
        <input type="text"   name="nome" placeholder="Seu nome" required>
        <input type="email"  name="email" placeholder="Seu email" required>
        <input type="text"   name="cep" placeholder="CEP" required>
        <input type="number" name="numero" placeholder="Número" required>
        <select name="tipo_endereco" required>
            <option value = "">Tipo de endereço</option>
            <option value = "empresa">Empresa</option>
            <option value = "condominio">Condomínio</option>
            <option value = "particular">Residência</option>
        </select>

        <input type="number" name="quantidade" placeholder="Quantidade de material" required>

        <button type="submit">Enviar Solicitação</button>

    </form>
</div>

</body>
</html>
