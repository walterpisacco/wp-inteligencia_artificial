<?php 
require_once '../../Utilidades/ClienteDAO.php';

$Func = new ClienteDAO();

$tipo 		= $_REQUEST['tipo'];
$param 		= $_REQUEST['param'];

$resultado = $Func->recuperarCombo($tipo,$param);

header("Content-type: application/json;charset=utf-8");
echo json_encode($resultado);