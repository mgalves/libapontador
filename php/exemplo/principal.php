<?php
/**
 * principal.php
 *
 * Tela principal da aplicação de exemplo, que permite a um usuário autenticado e autorizado
 * solicitar chamadas em seu nome à API. 
 *
 * Copyright 2010 Carlos Duarte do Nascimento (Chester)
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

require_once("../ApontadorApiLib.php");
require_once("db.php");

// Apenas usuários autenticados
session_start();
$login = $_SESSION["login"];
if (!$login) {
	header("Location: index.php");
}

$apontador_info = db_get_apontador_info($login);
extract($apontador_info);

// Processa ação, se houver
$acao = $_REQUEST["acao"];
if ($acao == "autorizar") {
	apontadorRedirectAutorizacao();
	die();
} else if ($acao == "logoff") {
	$_SESSION["login"] = null;
	header("Location: index.php");
	die();
} else if ($acao=="meus_dados") {
	$resultado = apontadorChamaApi("GET", "users/self", array("type"=>"json"), $oauth_token, $oauth_token_secret);
} else if ($acao=="minhas_avaliacoes") {
	$resultado = apontadorChamaApi("GET", "users/self/reviews", array("type"=>"json"), $oauth_token, $oauth_token_secret);
} else if ($acao=="busca_por_cep") {
	$resultado = apontadorChamaApi("GET", "search/places/byzipcode", array(
		"type"    => "json",
		"zip" => $_REQUEST["zipcode"],    // TODO remover
		"zipcode" => $_REQUEST["zipcode"],
		"radius"  => $_REQUEST["radius"],
		"term"  => $_REQUEST["term"]
	));
} else if ($acao=="inserir_avaliacao") {
	$PLACEID = $_REQUEST["PLACEID"];
	$resultado = apontadorChamaApi("PUT", "places/$PLACEID/reviews/new", array(
		"type"    => "json",
		"content" => $_REQUEST["content"],
		"rating"  => $_REQUEST["rating"]
	), $oauth_token, $oauth_token_secret);
} else if ($acao=="upload_foto") {
	$PLACEID = $_REQUEST["PLACEID"];
	$resultado = apontadorChamaApi("PUT", "places/$PLACEID/photos/new", array(
		"type"    => "json",
		"content" => base64_encode(file_get_contents($_FILES['foto']['tmp_name']))
	), $oauth_token, $oauth_token_secret);
}


?>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
	<h1>Aplicação Exemplo</h1>
	<form action="principal.php">
		<p>
			Olá, <?=$login?>. <input type="submit" name="acao" value="logoff" />
		</p>
		<p>
			<? if ($apontador_info["oauth_token"]) { ?>
				Você já autorizou esta aplicação no Apontador.
			<? } else { ?>
					Você não autorizou esta aplicação no Apontador.
					<input type="submit" name="acao" value="autorizar" />
			<? } ?>
		</p>	
		<? if ($resultado) { ?>
			<h2>Resultado</h2>
			<p>Resultado do último pedido:</p>
			<textarea rows="10" cols="80" readonly="readonly" scroll="both"><?=$resultado?></textarea><br/>
		<? } ?>
		
		<h2>Dados pessoais (requer autorização):</h2>
		<input type="submit" name="acao" value="meus_dados" />
		<input type="submit" name="acao" value="minhas_avaliacoes" /><br/>

	</form>
	<form action="principal.php">
		<h2>Busca local (por cep):</h2>
		O que: <input type="text" name="term"/>
		Cep: <input type="text" name="zipcode">
		Raio (m): <input type="text" name="radius" value="2000">
		<input type="submit" name="acao" value="busca_por_cep" /><br/>
		<br/>
	</form>
	<form action="principal.php">
		<h2>Cadastre uma avaliação</h2>
		<label for="PLACEID">PLACEID:</label>
		<input type="text" name="PLACEID" /><br/>
		<label for="content">Texto</label>
		<textarea name="content" cols="60" rows="4"></textarea><br/>
		<label for="rating">Nota:</label>
		<input type="radio" name="rating" value="1" checked="checked"/>1
		<input type="radio" name="rating" value="2"/>2
		<input type="radio" name="rating" value="3"/>3
		<input type="radio" name="rating" value="4"/>4
		<input type="radio" name="rating" value="5"/>5
		<input type="submit" name="acao" value="inserir_avaliacao" />
	</form>

	<form method="post" enctype="multipart/form-data" action="principal.php">
		<h2>Suba uma foto</h2>
		<label for="PLACEID">PLACEID:</label>
		<input type="text" name="PLACEID" /><br/>
		<label for="foto">Foto</label>
		<input type="file" name="foto" /><br/>
		<input type="submit" name="acao" value="upload_foto" />
		
	</form>
</body>
</html>
