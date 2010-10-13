<?php
/**
 * index.php
 *
 * Ponto de entrada da aplicação (apenas um formulário para login/cadastro)
 *
 * Copyright 2010 Apontador/LBS Local
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *    http: *www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */
?>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
	<h1>Aplicação Exemplo - Login</h1>
	<form action="cadastrologinaction.php">
		<label for="login">Login:</label>
		<input type="text" name="login" /><br/>
		<label for="senha">Senha:</label>
		<input type="password" name="senha" /><br/>
		<input type="submit" name="acao" value="login" />
		<input type="submit" name="acao" value="cadastrar" />
	</form>
</body>
</html>