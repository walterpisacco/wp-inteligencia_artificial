$(document).ready(function() {
	var pageWidth = $("#tblDatos").parent().width() - 100;	
	var formBuscar = $('#searchbox-events'),
	tbDatos = $("#tblDatos").jqGrid({
	    styleUI : 'Bootstrap',
		responsive : true,
		datatype : 'local',
		mtype : 'POST',
	    colNames: ['Codigo','idEquipo','Equipo','Dispositivo','Serie','Tipo','Cámara','Marca','Conexión','Modelo Aplicado','','','','','','',''],
	    colModel: [{name: 'celidDispositivo',hidden:true,index: '1',width: (pageWidth*(15/100)),align: 'center'},
	               {name: 'idEquipo',hidden:true,index: '2',width:(pageWidth*(20/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:4}},
	               {name: 'Equipo',index: '2',width:(pageWidth*(20/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:4}},
	               {name: 'Nombre',index: '2',width:(pageWidth*(40/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:4}},
	               {name: 'Serie',index: '3',width:(pageWidth*(20/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:3}},
	               {name: 'Tipo',index: '4',width:(pageWidth*(15/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Camara',hidden:true,index: '11',width:(pageWidth*(40/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Marca',index: '11',width:(pageWidth*(20/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'CamaraTipo',index: '11',width:(pageWidth*(14/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Modelos',index: '9',width:(pageWidth*(10/100)),align: 'center',editable:false,editoptions:{size:20,disabled:'disabled'},search:false,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Com1',hidden:true,index: '11',width:(pageWidth*(0/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Com2',hidden:true,index: '11',width:(pageWidth*(0/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Com3',hidden:true,index: '11',width:(pageWidth*(0/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Com4',hidden:true,index: '11',width:(pageWidth*(0/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Com5',hidden:true,index: '11',width:(pageWidth*(0/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Com6',hidden:true,index: '11',width:(pageWidth*(0/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:2}},
	         	   {name: 'acciones',index: '20',width:(pageWidth*(15/100)),align: 'left',editable:false,editoptions: {readonly: "readonly"}}], 
	               pager: '#pagDatos',
	    rowNum : 10,
	  //  altRows: true,
		autowidth : true,
		refresh: true,		
		height : 'auto',
		rownumbers : false,
		rowList : [ 10, 20, 30 ],
		sortname : 2,
		sortorder : 'ASC',
		viewrecords : true,
		gridview : true,
		caption : '',
		shrinkToFit : true,
		cellEdit: false,
       	cmTemplate : {
			'sortable' : false,
			'resize' : false,
			'editable' : true,
			'search' : false
		},
		rowattr:function(rowData){
		   if(rowData.estado == "Eliminado") return {"style":"color: lightcoral;"};
	    },
		loadComplete : function(data) {
		    $("tr.jqgrow:odd").addClass('myAltRowClassEven');
		    $("tr.jqgrow:even").addClass('myAltRowClassOdd');
		},
		loadError : function(xhr, st, err) {
			jQuery("#rsperror").html("Type: " + st + "; Response: "+ xhr.status + " " + xhr.statusText);
		}, /**/
		gridComplete : function(){
			$('#wrapper').on('toggle-out toggle-in',
					function(e) {
						tbDatos.trigger('resize');
					});
		}
	}).navGrid('#pagDatos', {edit : false,add : false,del : false,view : false,search : false,refresh : true});

if(isMobile.any()) {
	$("#tblDatos").hideCol("Equipo");	
	//$("#tblDatos").hideCol("Nombre");
	$("#tblDatos").hideCol("Serie");
	$("#tblDatos").hideCol("Tipo");
	$("#tblDatos").hideCol("Camara");
	$("#tblDatos").hideCol("Marca");
	$("#tblDatos").hideCol("CamaraTipos");
	$("#tblDatos").hideCol("Modelos");
	$("#tblDatos").hideCol("CamaraTipo");
	$("#tblDatos").setGridWidth($(window).width()-70); 
}

	function Buscar() {
		  var fields = formBuscar.find(':input').serializeArray();
	      var postdata = tbDatos.jqGrid('getGridParam', 'postData');
			    postdata.filters = formatFilter(fields);//La funcion esta en fngenerales
		        tbDatos.jqGrid('setGridParam', {
		        datatype: 'json',
		        url: "/DispositivosList_get",
				async:true,
	          stringResult: true,search: true,postData: postdata,page:1
	      }).trigger('reloadGrid');
	}

	Buscar();

	$.ajax({url:'/Combos_get',data:{tipo:'EQUIPOS',param:''},type:'POST',dataType:'json',async:true})
	.done(function(result){
	  if(result.length > 0){
	    $.each( result, function( key, value ) {
	      $('#equipo').append('<option value="'+value[0]+'" >'+value[1]+' ('+value[2]+')</option>');
	      $('#equipoBLE').append('<option value="'+value[0]+'" >'+value[1]+' ('+value[2]+')</option>');
	    });
	     $('#equipo').selectpicker('refresh');
	     $('#equipoBLE').selectpicker('refresh');
	  }
	});	

	$.ajax({url:'/Combos_get',data:{tipo:'TIPODSV',param:''},type:'POST',dataType:'json',async:true})
	.done(function(result){
	  if(result.length > 0){
	    $.each( result, function( key, value ) {
	      $('#tipo').append('<option value="'+value[0]+'" >'+value[1]+'</option>');
	      $('#tipoBLE').append('<option value="'+value[0]+'" >'+value[1]+'</option>');
	    });
	     $('#tipo').selectpicker('refresh');
	     $('#tipoBLE').selectpicker('refresh');
	  }
	});

	$.ajax({url:'/Combos_get',data:{tipo:'TIPOMARCAEQUIPO',param:''},type:'POST',dataType:'json',async:true})
	.done(function(result){
	  if(result.length > 0){
	    $.each( result, function( key, value ) {
	      $('#marca').append('<option value="'+value[0]+'" >'+value[1]+'</option>');
	      $('#marcaBLE').append('<option value="'+value[0]+'" >'+value[1]+'</option>');
	    });
	     $('#marca').selectpicker('refresh');
	     $('#marcaBLE').selectpicker('refresh');
	  }
	});	

	toggleGifLoad();
	// carga de modelos en el combo
	return $.ajax({url:'/DispositivoModelo_get',
		data : {},
		type:'POST',dataType:'json',async:true})
	 .always(toggleGifLoad)
	 .done(function(result){
	 	$("#modelo").empty();
	 	$('#modelo').append('<option value="0">Seleccione modelo...</option>');
		$.each( result, function( key, value ) {
			$('#modelo').append('<option data-tipo="'+value[1]+'" data-txt="'+value[3]+'" data-modelo="'+value[4]+'"  value="'+value[0]+'">'+value[2]+'</option>');
		});
		$('#modelo').append('<option data-tipo="alpr" data-txt="alpr.txt" data-modelo="alpr" value="-1">Reconocimiento de Patentes</option>');
        $('#modelo').selectpicker('refresh');
	 });

});	

function AgregarDispositivo(){
	limpiar();
	$('#modalDispositivo').modal('show');
}

$('#btnCamara').on('click',function(){
	$('#modalDispositivo').modal('hide');
	$('#modalEquipo').modal('show');
})

$('#btnBLE').on('click',function(){
	$('#modalDispositivo').modal('hide');	
	$('#modalBLE').modal('show');
})

$('#btnGuardarSalir').on('click',function(){
	bootbox.confirm({
	    message: '¿Esta seguro que desea guardar?',
	 //   locale: locale,		
	    buttons: {
	        confirm: {
	            className: 'btn-success'
	        },
	        cancel: {
	            className: 'btn-default'
	        }
	    },
	    callback: function (result) {
		    if(result == true){
		    	Grabar();
		    }
	    }
	});
});

function Grabar(){
	var dataform = {};
	dataform = $('#frmDispositivo  :input').serialize().replace(/["']/g, "");

	dataform += '&modeloDesc=' + $('#modelo option:selected').data("modelo");
	dataform += '&modeloTxt=' + $('#modelo option:selected').data("txt");
	
	if($('#view').bootstrapSwitch('status') == true){
		dataform += '&view=si';	
	}else{
		dataform += '&view=no';
	}
	if($('#dron').bootstrapSwitch('status') == true){
		dataform += '&dron=si';
	}else{
		dataform += '&dron=no';
	}

    if (validateFields($('#frmDispositivo :input').not('button'))){
    	bootbox.alert('Los campos marcados, son obligatorios');
    	return;
    }

	toggleGifLoad();
		return $.ajax({url:'/Dispositivo_Guardar',
			data:dataform,
			type:'POST',dataType:'json',async:true})
		 .always(toggleGifLoad)
		 .done(function(result){
			 if (result[0][1] == 'true'){
		 		//bootbox.alert({ message:result[0][0],backdrop: true});
			 	//$('#modalEquipo').modal('hide');
		 		$('#tblDatos').trigger("reloadGrid");
			 }else{
			 	bootbox.alert({ message:'ERROR AL INTENTAR GRABAR, INTENTE NUEVAMENTE!!',backdrop: true});
			 }
		 }); 
}

function EliminarDispositivo(){
	selRowId = $("#tblDatos").jqGrid ('getGridParam', 'selrow');
	idDispositivo = $("#tblDatos").jqGrid ('getCell', selRowId, 'celidDispositivo');
	bootbox.confirm({
    message: '¿Esta seguro que desea eliminar?',
 //   locale: locale,		
    buttons: {
        confirm: {
            className: 'btn-success'
        },
        cancel: {
            className: 'btn-default'
        }
    },
    callback: function (result) {
	    if(result == true){
	    	Eliminar(idDispositivo);
	    }
    }
	});
}

function Eliminar(idDispositivo){
	toggleGifLoad();
		return $.ajax({url:'/Dispositivo_Eliminar',
			data:{idDispositivo:idDispositivo},
			type:'POST',dataType:'json',async:true})
		 .always(toggleGifLoad)
		 .done(function(result){
			 if (result[0][1] == 'true'){
		 		bootbox.alert({ message:result[0][0],backdrop: true});
		 		$('#tblDatos').trigger("reloadGrid");			 	
			 }
		 }); 
}

function EditarBLE(){
	limpiar();
	selRowId = $("#tblDatos").jqGrid ('getGridParam', 'selrow');
    celidDispositivo = $("#tblDatos").jqGrid ('getCell', selRowId, 'celidDispositivo');
    celidEquipo = $("#tblDatos").jqGrid ('getCell', selRowId, 'idEquipo');
    celTipo = $("#tblDatos").jqGrid ('getCell', selRowId, 'Tipo');
    celMarca = $("#tblDatos").jqGrid ('getCell', selRowId, 'Marca');
    celNombre = $("#tblDatos").jqGrid ('getCell', selRowId, 'Nombre');
    celSerie = $("#tblDatos").jqGrid ('getCell', selRowId, 'Serie');
    
    $('#idBLE').val(celidDispositivo);

	$('#equipoBLE option[value='+celidEquipo+']').prop('selected', true);
	$('#equipoBLE').selectpicker('refresh');

	$("#tipoBLE").find('option:contains("'+celTipo+'")').prop('selected', true);
	$('#select2-tipoBLE-container').text( $('#tipoBLE option:selected').text());
	$('#tipoBLE').selectpicker('refresh');

	$("#marcaBLE").find('option:contains("'+celMarca+'")').prop('selected', true);
	$('#select2-marcaBLE-container').text( $('#marcaBLE option:selected').text());
	$('#marcaBLE').selectpicker('refresh');	

	$('#nombreBLE').val(celNombre);	
	$('#serieBLE').val(celSerie);	

	$('#modalBLE').modal('show');
}

function EditarCamara(){
	limpiar();
	selRowId = $("#tblDatos").jqGrid ('getGridParam', 'selrow');
    celidDispositivo = $("#tblDatos").jqGrid ('getCell', selRowId, 'celidDispositivo');
    celidEquipo = $("#tblDatos").jqGrid ('getCell', selRowId, 'idEquipo');
    celEquipo = $("#tblDatos").jqGrid ('getCell', selRowId, 'Equipo');
    celNombre = $("#tblDatos").jqGrid ('getCell', selRowId, 'Nombre');
    celSerie = $("#tblDatos").jqGrid ('getCell', selRowId, 'Serie');
    celTipo = $("#tblDatos").jqGrid ('getCell', selRowId, 'Tipo');
    celCamara = $("#tblDatos").jqGrid ('getCell', selRowId, 'Camara');
    celMarca = $("#tblDatos").jqGrid ('getCell', selRowId, 'Marca');
    celCamaraTipo = $("#tblDatos").jqGrid ('getCell', selRowId, 'CamaraTipo');
    celCom1 = $("#tblDatos").jqGrid ('getCell', selRowId, 'Com1');
    celCom2 = $("#tblDatos").jqGrid ('getCell', selRowId, 'Com2');
    celCom3 = $("#tblDatos").jqGrid ('getCell', selRowId, 'Com3');
    celCom4 = $("#tblDatos").jqGrid ('getCell', selRowId, 'Com4');
    celCom5 = $("#tblDatos").jqGrid ('getCell', selRowId, 'Com5');
    celCom6 = $("#tblDatos").jqGrid ('getCell', selRowId, 'Com6');

	$('#spDispositivo').text(celNombre);
	$('#idDispositivo').val(celidDispositivo);
	$('#nombre').val(celNombre);	
	$('#serie').val(celSerie);

	$('#equipo option[value='+celidEquipo+']').prop('selected', true);
	$('#equipo').selectpicker('refresh');

	$("#marca").find('option:contains("'+celMarca+'")').prop('selected', true);
	$('#select2-marca-container').text( $('#marca option:selected').text());
	$('#marca').selectpicker('refresh');

	if(celCamaraTipo == 'webcam'){
		$('#webcamInput option[value='+celCamara+']').prop('selected', true);
		$('#webcamInput').selectpicker('refresh');
		$('#ruta').css('display','none');
		$('#btnSubir').css('display','none');
	}else{ // si es rtsp coloco la direccion
		$('#ruta').val(celCamara);
		$('#ruta').css('display','');
		$('#btnSubir').css('display','none');
		$('#webcamInput option[value=4]').prop('selected', true);
		$('#webcamInput').selectpicker('refresh');
	}

	$('#comu1').val(celCom1);
	$('#comu2').val(celCom2);
	$('#comu3').val(celCom3);
	$('#comu4').val(celCom4);
	$('#comu5').val(celCom5);
	$('#comu6').val(celCom6);

	$('#modalEquipo').modal('show');
}

function EditarDispositivo(){
	selRowId = $("#tblDatos").jqGrid ('getGridParam', 'selrow');
    celCamaraTipo = $("#tblDatos").jqGrid ('getCell', selRowId, 'CamaraTipo');

    if(celCamaraTipo == 'webcam' || celCamaraTipo == 'rtsp'){
    	EditarCamara();
    }

    if(celCamaraTipo == 'ble'){
    	EditarBLE();
    }
	
};

$('#modelo').on('change',function(){
	$("#analitica").empty();
	$('#analitica').selectpicker('refresh');
	txtmodelo = $('#modelo option:selected').data("txt");
	tipomodelo = $('#modelo option:selected').data("tipo");
/*
	if(tipomodelo=='pickle'){
		$('.slider').html('<div class="slide-track"></div>');
	}

	if(tipomodelo=='alpr'){
		$('.slider').html('<img src="/static/graph/patente1.png">');
	}
*/
	$.ajax({url:'/labels',data:{txtmodelo:txtmodelo},type:'POST',dataType:'json',async:true})
	.done(function(result){
	  if(result.length > 0){
	    $.each( result, function( key, value ) {
	      $('#analitica').append('<option value="'+value[0]+'" >'+value[1]+'</option>');
	    });
	     $('#analitica').selectpicker('refresh');
	  }
	});
})

$("#uploadedFile").change(function(){
	$('#ruta').val($('#uploadedFile')[0].files[0].name);
});

$('#btnEjecutar').on('click',function(){
	Reproducir();		    	
});

function Reproducir(){
		var camera = 0;

		if($('#webcamInput').val() <= 3 ) {
			camera = $('#webcamInput').val();
		}
		if($('#webcamInput').val() == 4 ) {
			camera = $('#ruta').val();
		}
		if($('#webcamInput').val() ==5 || $('#webcamInput').val() ==6 ) {
			camera = $('#ruta').val();
		}

		var serie 	= $('#serie').val();
		var tipo 	= $('#modelo option:selected').data("tipo");
		var webcamId= $('#webcamInput option:selected').val();
		var label 	= $('#modelo option:selected').data("txt");
		var modelo 	= $('#modelo option:selected').data("modelo");
		var opcion 	= $('#analitica option:selected').val();

		if($('#view').bootstrapSwitch('status') == true){
			var iot = 1;
		}else{
			var iot = 0;
		}

		$.ajax({
			data : {
				serie : serie,
				webcam : camera,
				webcamId : webcamId,
				tipo : tipo,
				label : label,
				modelo : modelo,
				opcion : opcion,
				iot: iot
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			} else {
				d = new Date();
				$('#video_validado').find('img').attr("src", "/video_feed?"+d.getTime());
				$('#errorAlert').hide();
			}
		});
		event.preventDefault();
}

$('#btnCerrar').on('click',function(){
	Detener();
})

function Detener(){
	$.ajax({data : {},type : 'GET',url : '/video_feed_detener'});
	event.preventDefault();
}

$('#webcamInput').on('change',function(){
	if($('#webcamInput option:selected').val() < 5){
		$('#ruta').prop('placeholder','');
		$('#ruta').css('display','none');
		$('#btnSubir').css('display','none');
	}	
	if($('#webcamInput option:selected').val()== 4){
		$('#ruta').prop('placeholder','ingresar dirección rtsp');
		$('#ruta').css('display','');
		$('#btnSubir').css('display','none');
	}
	if($('#webcamInput option:selected').val()== 5){
		$('#ruta').prop('placeholder','seleccionar ruta del archivo');
		$('#ruta').css('display','');
		$('#ruta').val('');
		$('#btnSubir').css('display','');		
	}

	if($('#webcamInput option:selected').val()== 6){
		$('#ruta').prop('placeholder','pegar link de youtube');
		$('#ruta').css('display','');
		$('#ruta').val('');
		$('#btnSubir').css('display','none');

	}
})

$('#btnGuardarBLE').on('click',function(){
	bootbox.confirm({
	    message: '¿Esta seguro que desea guardar?',
	 //   locale: locale,		
	    buttons: {
	        confirm: {
	            className: 'btn-success'
	        },
	        cancel: {
	            className: 'btn-default'
	        }
	    },
	    callback: function (result) {
		    if(result == true){
		    	GrabarBLE();
		    }
	    }
	});
});

function GrabarBLE(){
	var dataform = {};
	dataform = $('#frmBLE  :input').serialize().replace(/["']/g, "");
    if (validateFields($('#frmBLE :input').not('button'))){
    	bootbox.alert('Los campos marcados, son obligatorios');
    	return;
    }
	toggleGifLoad();
		return $.ajax({url:'/DispositivoBLE_Guardar',
			data:dataform,
			type:'POST',dataType:'json',async:true})
		 .always(toggleGifLoad)
		 .done(function(result){
			 if (result[0][1] == 'true'){
		 		bootbox.alert({ message:result[0][0],backdrop: true});
			 	$('#modalBLE').modal('hide');
		 		$('#tblDatos').trigger("reloadGrid");
			 }else{
			 	bootbox.alert({ message:'ERROR AL INTENTAR GRABAR, INTENTE NUEVAMENTE!!',backdrop: true});
			 }
		 }); 
}

$( ".modal-dialog" ).draggable();

function Entrenar(){
	selRowId = $("#tblDatos").jqGrid ('getGridParam', 'selrow');
    celNombre = $("#tblDatos").jqGrid ('getCell', selRowId, 'Nombre');
    celCamara = $("#tblDatos").jqGrid ('getCell', selRowId, 'Camara');
	$('#spEntrenar').text(celNombre);
	$('#idCamara').val(celCamara);
	$('#modalEntrenar').modal('show');
	//ReproducirOffLine();

};

$('#btnFotograma').on('click',function(){

})

$('#btnVideo').on('click',function(){
	ReproducirOffLine('video');
	$('#btnDetener').css('display','');	
})

$('#btnDetener').on('click',function(){
			$.ajax({
			data : {},
			type : 'GET',
			url : '/video_feed_detener'
		});
		$('#btnDetener').css('display','none');
})

	// carga imagenes del carrousel
	$.ajax({url:'/Imagen_Buscar',
		data : {},
		type:'GET',dataType:'json',async:true})
	 .done(function(result){
	 	$(".slide-track").empty();
		$.each( JSON.parse(result), function( key, value ) {
	 		$(".slide-track").append('<div class="slide"> <img src="'+value['imagen']+'" style="width:120px" alt="name" class="imgCarrousel"></div>');
		});
	});

function limpiar(){
	$('.limp').val('');
	$('.limp').text('');
	$('#idDispositivo').val(0);
	$('#idBLE').val(0);	

}


