<?php
/**
 * db.php
 *
 * Guarda/recupera usuários no banco de dados, autenticando associando dados de acesso da API a eles.
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

/**
 * Insere um usuário no banco
 *
 * @param string login
 * @param string senha
 * @return false se ocorrer um problema (ex.: usuário já existe). 
 */
function db_cadastra($login, $senha) {
	$db = _db_get_db();
	return sqlite_query($db, "INSERT INTO usuarios (login, senha) VALUES ('" . $login . "','" . $senha . "')");
}

/**
 * Verifica se login e senha de um usuário conferem
 *
 * @param string login
 * @param string senha
 * @return false se ocorrer um problema (ex.: senha inválida ou usuário não existe). 
 */
function db_login($login, $senha) {
	$db = _db_get_db();
	return sqlite_fetch_array(
		sqlite_query($db, "SELECT login FROM usuarios WHERE login='" . $login . "' AND senha='" . $senha . "'")
	);
}


/**
 * Recupera os dados do Apontador associados a um login
 *
 * @return mixed oauth_token, oauth_token_secret e user_id (null/false se login não existe).
 */
function db_get_apontador_info($login) {
	$db = _db_get_db();
	$result = sqlite_query($db, "SELECT oauth_token, oauth_token_secret, user_id FROM usuarios WHERE login='" . $login . "'");
	$result_data = sqlite_fetch_array($result);
	if ($result_data) {
		return array(
			"oauth_token" => $result_data["oauth_token"],
			"oauth_token_secret" => $result_data["oauth_token_secret"],
			"user_id" => $result_data["user_id"]
		);
	}
}

/**
 * Associa dados do Apontador a um login
 *
 * @param string login usuário ao qual os dados serão associados
 * @param string oauth_token
 * @param string oauth_token_secret
 * @param string user_id
 */
function db_set_apontador_info($login, $oauth_token, $oauth_token_secret, $user_id) {
	$db = _db_get_db();
	return sqlite_exec($db, "UPDATE usuarios SET oauth_token='$oauth_token',oauth_token_secret='$oauth_token_secret',user_id='$user_id' WHERE login='$login'");
}

/**
 * Recuperando o objeto de acesso ao banco (criando ele e a tabela, se necessário).
 *
 * @return var objeto de acesso ao banco
 */
function _db_get_db(){
	$banco_novo = !file_exists("banco");
	if (!$db = sqlite_open("banco")) {
		die($sqliteerror);
	};
	if ($banco_novo) {
		sqlite_query($db, "CREATE TABLE usuarios (login varchar(50) PRIMARY KEY, senha varchar(50), oauth_token varchar(500), oauth_token_secret varchar(500), user_id varchar(20));");
	}
	return $db;
}
	
