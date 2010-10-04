<?php
/**
 * callback.php
 *
 * Processa o retorno de uma autorização de uso.
 */

require_once("../ApontadorApiLib.php");
require_once("db.php");

// Identifica o usuário do nosso sistema que voltou do Apontador
session_start();
$login = $_SESSION["login"];
if (!$login) {
	die("Sessão inválida");
}

// Se tudo der certo, temos um token pra acessar a API no nome dele
$access_token = apontadorProcessaAutorizacao();
if (!$access_token) {
	die("Acesso inválido");
}

// Guarda o token no banco, para o usuário não ter que passar por isso novamente e manda
// ele para a tela principal.
extract($access_token);
db_set_apontador_info($login, $oauth_token, $oauth_token_secret, $user_id);
header("Location: principal.php");
