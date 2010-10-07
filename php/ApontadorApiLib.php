<?php
/**
 * ApontadorApiLib.php
 *
 * Encapsulamento (bem simplificado) dos mecanismos de chamada oAuth à Apontador API.
 * Configure os dados da sua aplicação no ApontadorApiConfig antes de usar.
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

require_once("ApontadorApiConfig.php");
require_once("OAuth.php");

/**
 * Leva o usuário  para o site Apontador, para que ele autorize a aplicação. Deve ser
 * a última coisa chamada na página (vai mandar um redirect).
 */
function apontadorRedirectAutorizacao() {
	
	extract(apontadorGetConfig());
	$consumer = new OAuthConsumer($key, $secret, NULL);
	$signature_method = new OAuthSignatureMethod_HMAC_SHA1();

 	// Passo 1: Pedir o par de tokens inicial (oauth_token e oauth_token_secret) para o Apontador
	$endpoint = "http://api.apontador.com.br/v1/oauth/request_token";
	$req_req = OAuthRequest::from_consumer_and_token($consumer, NULL, "GET", $endpoint, array());
	$req_req->sign_request($signature_method, $consumer, NULL);
	parse_str(file_get_contents($req_req));
	
	// Passo 2: Redirecionar o usuário para o Apontador, para que ele autorize o uso dos seus dados.
	$endpoint = "http://api.apontador.com.br/v1/oauth/authorize";
	$oauth_callback = "$callbackurl?&key=$key&secret=$secret&token=$oauth_token&token_secret=$oauth_token_secret&endpoint=" . urlencode($endpoint);
	$auth_url = $endpoint . "?oauth_token=$oauth_token&oauth_callback=" . urlencode($oauth_callback) . "";
	header("Location: $auth_url");
	
}

/**
 * Processa o retorno (callback) de uma autorização, obtendo os dados de acesso definitivos
 * (token+secret) e o ID do usuário.
 *
 * A função acessa diretamente o request ($_REQUEST) para obter os dados.
 *
 * @return mixed dados de acesso (oauth_token e oauth_token_secret) e user_id do Apontador.
 */
function apontadorProcessaAutorizacao() {

	extract(apontadorGetConfig());
	$consumer = new OAuthConsumer($key, $secret, NULL);
	$signature_method = new OAuthSignatureMethod_HMAC_SHA1();

	$token = $_REQUEST["oauth_token"];
	$verifier = $_REQUEST["oauth_verifier"];
	if ((!$token) || (!$verifier)) {
		return null;
	}

	// Passo 3: Passa o token e verificador para o Apontador, que vai validar o callback
	//          e devolver o token de acesso definitivo
	$endpoint = "http://api.apontador.com.br/v1/oauth/access_token?oauth_verifier=$verifier";
	$parsed = parse_url($endpoint);
	$params = array();
	parse_str($parsed['query'], $params);
	$acc_req = OAuthRequest::from_consumer_and_token($consumer, NULL, "GET", $endpoint, $params);
	$acc_req->sign_request($signature_method, $consumer, NULL);
	parse_str(file_get_contents($acc_req), $access_token);
	return $access_token;

}

/**
 * Efetua uma chamada a um método API
 *
 * @param verbo string GET, POST, PUT ou DELETE, conforme o método/intenção
 * @param metodo string path do métdodo, sem "/" no começo (ex.: "users/self")
 * @param params mixed parâmetros da chamada (array associativo)
 * @param oauth_token string token de autorização do usuário. Se omitido, a chamada usa HTTP Basic Auth
 * @param oauth_token_secret string secret do token de autorização do usuário (ignorado se oauth_token não for passado)
 * @return resultado da chamada.
 */                    
function apontadorChamaApi($verbo="GET", $metodo, $params=array(), $oauth_token="", $oauth_token_secret="") {
   
	extract(apontadorGetConfig());
	$endpoint = "http://api.apontador.com.br/v1/$metodo";
	if (!$oauth_token) {
		$queryparams = http_build_query($params);
		$auth_hash = base64_encode("$email:$key");
		return _post("$endpoint?$queryparams", "GET", null, "Authorization: $auth_hash");
	} else {
		// OAuth
		$consumer = new OAuthConsumer($key, $secret, NULL);
		$token = new OAuthConsumer($oauth_token, $oauth_token_secret);
		$signature_method = new OAuthSignatureMethod_HMAC_SHA1();
		$req_req = OAuthRequest::from_consumer_and_token($consumer, $token, $verbo, $endpoint, $params);
		$req_req->sign_request($signature_method, $consumer, $token);
		if ($verbo=="GET") {
			return _post($req_req, $verbo);
		} else {
			return _post($endpoint, $verbo, $req_req->to_postdata());
		}
	}
}



function _post($url, $method, $data = null, $optional_headers = null)
{
	$params = array('http' => array(
					'method' => $method,
					'ignore_errors' => true
				));
	if ($optional_headers !== null) {
		$params['http']['header'] = $optional_headers;
	}
	if ($data !== null) {
		$params['http']['content'] = $data;
	}
	$ctx = stream_context_create($params);
	$fp = @fopen($url, 'rb', false, $ctx);
	$response = @stream_get_contents($fp);
	return $response;
}
