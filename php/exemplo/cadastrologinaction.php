<?php
/**
 * cadastrologinaction.php
 *
 * Processa o form inicial, cadastrando ou autenticando o usuário.
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

require_once("db.php");
require_once("../ApontadorApiLib.php");

// Se o cadastro ou login for bem sucedido, guarda na sessão
if ($_REQUEST["acao"]=="cadastrar") {
	if (!db_cadastra($_REQUEST["login"], $_REQUEST["senha"])) {
		die("Erro no cadastro (login ja existe?)");
	}
} else {
	if (!db_login($_REQUEST["login"], $_REQUEST["senha"])) {
		die("Erro no login (usuario/senha conferem?)");
	}
};
session_start();
$_SESSION["login"] = $_REQUEST["login"];
		
// Pode ir para a tela principal
header("Location: principal.php");

